# This file is part of Indico.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from datetime import date, timedelta
from uuid import uuid4

from sqlalchemy.dialects.postgresql import JSON

from indico.core.db import db
from indico.modules.events.surveys.models.items import SurveyQuestion, SurveySection
from indico.modules.events.surveys.models.submissions import SurveyAnswer, SurveySubmission
from indico.modules.events.surveys.models.surveys import Survey

from indico_migrate.steps.events import EventMigrationStep
from indico_migrate.util import convert_to_unicode, sanitize_user_input


class EventSurveyImporter(EventMigrationStep):
    step_id = 'survey'

    def __init__(self, *args, **kwargs):
        super(EventSurveyImporter, self).__init__(*args, **kwargs)

    def initialize_global_ns(self, g):
        g.legacy_survey_mapping = {}

    def migrate(self):
        evaluations = getattr(self.conf, '_evaluations', [])
        assert len(evaluations) < 2

        if evaluations and evaluations[0]._questions:
            survey = self.migrate_survey(evaluations[0])
            self.global_ns.legacy_survey_mapping[self.conf] = survey
            db.session.add(survey)
            db.session.flush()

    def migrate_survey(self, evaluation):
        survey = Survey(event=self.event)
        title = convert_to_unicode(evaluation.title)
        if title and not title.startswith('Evaluation for '):
            survey.title = sanitize_user_input(title)
        if not survey.title:
            survey.title = "Evaluation"
        survey.introduction = sanitize_user_input(evaluation.announcement)
        if evaluation.contactInfo:
            contact_text = "Contact: ".format(sanitize_user_input(evaluation.contactInfo))
            survey.introduction += "\n\n{}".format(contact_text) if survey.introduction else contact_text
        survey.submission_limit = evaluation.submissionsLimit if evaluation.submissionsLimit else None
        survey.anonymous = evaluation.anonymous
        # Require the user to login if the survey is not anonymous or if logging in was required before
        survey.require_user = not survey.anonymous or evaluation.mandatoryAccount

        if evaluation.startDate.date() == date.min or evaluation.endDate.date() == date.min:
            survey.start_dt = self.event.end_dt
            survey.end_dt = survey.start_dt + timedelta(days=7)
        else:
            survey.start_dt = self._naive_to_aware(evaluation.startDate)
            survey.end_dt = self._naive_to_aware(evaluation.endDate)
        if survey.end_dt < survey.start_dt:
            survey.end_dt = survey.end_dt + timedelta(days=7)

        for kind, notification in evaluation.notifications.iteritems():
            survey.notifications_enabled = True
            recipients = set(notification._toList) | set(notification._ccList)
            if kind == 'evaluationStartNotify':
                survey.start_notification_emails = list(recipients)
            elif kind == 'newSubmissionNotify':
                survey.new_submission_emails = list(recipients)

        self.print_success('%[cyan]{}%[reset]'.format(survey))

        question_map = {}
        section = SurveySection(survey=survey, display_as_section=False)
        for position, old_question in enumerate(evaluation._questions):
            question = self.migrate_question(old_question, position)
            question_map[old_question] = question
            section.children.append(question)

        for i, old_submission in enumerate(evaluation._submissions, 1):
            submission = self.migrate_submission(old_submission, question_map, i)
            survey.submissions.append(submission)
        survey._last_friendly_submission_id = len(survey.submissions)

        return survey

    def migrate_question(self, old_question, position):
        question = SurveyQuestion()
        question.position = position
        question.title = sanitize_user_input(old_question.questionValue)
        question.description = sanitize_user_input(old_question.description)
        if old_question.help:
            help_text = sanitize_user_input(old_question.help)
            question.description += "\n\nHelp: {}".format(help_text) if question.description else help_text
        question.is_required = old_question.required
        question.field_data = {}
        class_name = old_question.__class__.__name__
        if class_name == 'Textbox':
            question.field_type = 'text'
        elif class_name == 'Textarea':
            question.field_type = 'text'
            question.field_data['multiline'] = True
        elif class_name == 'Password':
            question.field_type = 'text'
        elif class_name in ('Checkbox', 'Radio', 'Select'):
            question.field_data['options'] = []
            question.field_type = 'single_choice' if class_name in ('Radio', 'Select') else 'multiselect'
            if question.field_type == 'single_choice':
                question.field_data['display_type'] = class_name.lower()
            if class_name == 'Radio':
                question.field_data['radio_display_type'] = 'vertical'
            for option in old_question.choiceItems:
                question.field_data['options'].append({'option': option, 'id': unicode(uuid4())})
        self.print_success(" - Question: {}".format(question.title))
        return question

    def migrate_submission(self, old_submission, question_map, friendly_id):
        submitter = old_submission._submitter
        if not old_submission.anonymous and submitter is not None:
            user = self.global_ns.avatar_merged_user[submitter.id]
        else:
            user = None

        submission = SurveySubmission(is_submitted=True, is_anonymous=(user is None), user=user,
                                      friendly_id=friendly_id)
        submitted_dt = old_submission.submissionDate
        submission.submitted_dt = submitted_dt if submitted_dt.tzinfo else self._naive_to_aware(submitted_dt)
        self.print_success(" - Submission from user {}".format(submission.user or 'anonymous'))
        for old_answer in old_submission._answers:
            question = question_map[old_answer._question]
            answer = self.migrate_answer(old_answer, question)
            submission.answers.append(answer)
            question.answers.append(answer)
        return submission

    def migrate_answer(self, old_answer, question):
        answer = SurveyAnswer(data=JSON.NULL)
        if old_answer.__class__.__name__ == 'MultipleChoicesAnswer':
            answer.data = []
            for option in old_answer._selectedChoiceItems:
                answer.data.append(self._get_option_id(question, option))
        elif old_answer._question.__class__.__name__ in ('Radio', 'Select'):
            if old_answer._answerValue:
                answer.data = self._get_option_id(question, old_answer._answerValue)
        else:
            answer.data = sanitize_user_input(old_answer._answerValue)
        self.print_success("   - Answer: {}".format(answer.data))
        return answer

    def _get_option_id(self, question, option):
        return next((opt['id'] for opt in question.field_data['options'] if opt['option'] == option), None)
