
//this automatically executes
! function () {
    window.modules = {};

    window.modules.ToasterFactory = function (domOrFrag) {
        var dom = domOrFrag || document,
            Toaster = function () {
                var self = this;
                this.timeToHide = 5000;
                this.toast = dom.getElementById('toast') || undefined;

                this.show = function() {
                    if (this.toast) {
                        this.toast.classList.add('cts-toast--active');
                    }
                };

                this.hide = function() {
                    if (this.toast) {
                        this.toast.classList.remove('cts-toast--active');
                    }
                };

                this.flash = function(finishedCallback) {
                    this.show();
                    window.setTimeout(function () {
                        self.hide();
                        if (typeof finishedCallback === 'function') {
                            finishedCallback();
                        }
                    }, this.timeToHide);
                };

                this.changeDOM = function (dom) {
                    this.toast = dom.getElementById('toast');
                };
            };

        return new Toaster();
    };

    window.Toaster = window.modules.ToasterFactory(document);

    window.Toaster.flash();

//////////////
//end toast
//////////////


    window.modules.TaggerFactory = function (domOrFrag) {
        var dom = domOrFrag || document,
            Tagger = function () {
                var self = this;

                this.addValue = function (name, val) {
                    var hiddenInputNode = document.getElementById('tag-input_' + name),
                        values = hiddenInputNode.value.split(';');
                    values.push(val);
                    hiddenInputNode.value = values.join(';');
                };

                this.deleteTag = function (event) {
                    var removeMe = event.target.parentElement,
                        value = event.target.parentElement.children[0].textContent,//the li
                        parent = removeMe.parentElement;
                    self.removeValue(self.getTagboxName(event.target), value);
                    parent.removeChild(removeMe);
                };

                this.removeValue = function (name, val) {
                    var hiddenInputNode = document.getElementById('tag-input_' + name),
                        values = hiddenInputNode.value.split(';');
                    values = values.filter((item) => item !== val);
                    hiddenInputNode.value = values.join(';');
                };

                this.getTagboxName = function (node) {
                    if (node.parentElement) {
                        if (node.hasAttribute('data-name')) {
                            return node.getAttribute('data-name');
                        } else {
                            return self.getTagboxName(node.parentElement);
                        }
                    }
                };

                this.createtag = function(text) {
                    var container = document.createElement('div'),
                        li = document.createElement('li'),
                        tagDelete = document.createElement('i'),
                        icontext = document.createTextNode('cancel'),
                        tagtext = document.createTextNode(text);

                    container.appendChild(li);
                    container.appendChild(tagDelete);
                    li.appendChild(tagtext);
                    tagDelete.appendChild(icontext);

                    li.classList.add('tag');
                    tagDelete.classList.add('tiny');
                    tagDelete.classList.add('tag__delete');
                    container.classList.add('tag__container');

                    tagDelete.addEventListener('click', function(event) {
                        event.preventDefault();
                        self.deleteTag(event);
                    });

                    return container;
                };

                this.addTag = function(inputNode) {
                    var text = inputNode.value.trim(),
                        name = getTagboxName(inputNode),
                        tagHolderId = 'tag-holder_' + name,
                        key;

                    if (text) {
                        tag = self.createtag(text);
                        self.addValue(name, text);
                        document.getElementById(tagHolderId).appendChild(tag);
                        inputNode.value = "";
                    }
                };

                this.tagboxEventListenerPairs = [
                    {
                        event: 'keyup',
                        listener: function(event) {
                            event.preventDefault();
                            if (event.keyCode == 13) {
                                self.addTag(this);
                            }
                        }
                    },
                    {
                        event: 'blur',
                        listener: function(event) {
                            event.preventDefault();
                            self.addTag(this);
                        }
                    },
                    {
                        event: 'input',
                        listener: function(event) {
                            var invisibleSpace = '\u200B';
                            if (event.target.value.includes(invisibleSpace)){
                                self.addTag(this);
                            }
                            return true;
                        }
                    }
                ];

                this.findInputsTags = function () {
                    this.tagboxInputs = dom.getElementsByClassName('tagbox__input');
                    this.deleteTags = dom.getElementsByClassName("tag__delete");
                };

                this.attachEventListeners = function() {
                    Array.prototype.forEach.call(this.tagboxInputs, function (node) {
                        self.tagboxEventListenerPairs.forEach(function (item) {
                            node.addEventListener(item.event, item.listener);
                        });
                    });
                    Array.prototype.forEach.call(this.deleteTags, function (node) {
                        node.addEventListener('click', self.deleteTag);
                    });
                };
            };

        return new Tagger();
    };

    window.Tagger = window.modules.TaggerFactory(document);
    window.Tagger.findInputsTags();
    window.Tagger.attachEventListeners();

    $('.datepicker').pickadate({
        formatSubmit: 'yyyy-mm-dd',
        hiddenName: true,
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15, // Creates a dropdown of 15 years to control year
    });

    $('.modal-trigger').leanModal();

    window.submit_answer = function (questionId, projectId, choiceId) {
        window.$.ajax('/answer_submit/', {
            method: 'POST',
            data: {
                choice_id: choiceId,
                project_id: projectId,
                question_id: questionId,
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            }
        });
    };

}();
