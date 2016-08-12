from approver.models import Question, Section
from approver.utils import get_related

class QuestionForm():

    def __init__(self, project_id=None, question_section_name='Wisconsin questions'):
        self.project_id = project_id
        self.form_section = Section.objects.get(name=question_section_name)
        self.question_list = self.get_questions(self.form_section)

    def get_question_tag_context(self, question_model):
        return {
            'question_text': question_model.text,
            'question_id': question_model.id,
            'question_description': question_model.description,
            'answers': [self.get_choice_dict(choice) for choice in question_model.choice.all()],
            'sort_order': question_model.sort_order,
            'project_id': self.project_id,
        }

    def get_sorted_questions(self):
        # this is js syntax probably doesnt work in django
        self.question_list.sort(key=lambda k: k['sort_order'])
        return self.question_list

    def get_questions(self, section):
        question_models = Question.objects.filter(section=section)
        return [self.get_question_tag_context(question) for question in question_models]

    def get_choice_dict(self, choice):
        return {
            'text': choice.text,
            'id': choice.id,
        }
