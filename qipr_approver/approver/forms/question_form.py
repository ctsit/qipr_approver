
class QuestionForm():

    # eventually generate these questions and their respective answers from
    # some database information.
    def __init__(self):
        # make a separate templatetag for answers? something that can
        # determine what type of thing to use? ie radio checkbox etc
        self.question_list = [
            {'question_text':'whats your favorite color',
             'answer_choices':['red', 'green', 'blue'],
             'order':1}
        ]

    def get_sorted_questions(self):
        # this is js syntax probably doesnt work in django
        self.question_list.sort(key=lambda k: k['order'])
        return self.question_list
