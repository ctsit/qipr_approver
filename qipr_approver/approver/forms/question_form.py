from approver.models import Question
from approver.utils import get_related_property
class QuestionForm():

    def __init__(self):
        # make a separate templatetag for answers? something that can
        # determine what type of thing to use? ie radio checkbox etc

        self.question_list = [self.get_question_tag_context(question) for question in Question.objects.all()]

    def get_question_tag_context(self, question_model):
        return {
            'question_text': question_model.text,
            'question_id': question_model.id,
            'question_description': question_model.description,
            'answers': get_related_property(question_model, 'choice', 'text'),
            'sort_order': question_model.sort_order,
        }

    def get_sorted_questions(self):
        # this is js syntax probably doesnt work in django
        self.question_list.sort(key=lambda k: k['sort_order'])
        return self.question_list
