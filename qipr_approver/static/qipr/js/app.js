
//this automatically executes
! function () {

    window.Toaster = function () {
        var timeToShow = 500,
            timeToHide = 5000,
            Toaster = function () {
                var self = this;
                this.toast = document.getElementById('toast') || undefined;

                this.show = () => {
                    window.setTimeout(function () {
                        if (self.toast) {
                            self.toast.classList.add('cts-toast--active');
                        }
                    }, timeToShow);
                };

                this.hide = () => {
                    window.setTimeout(function () {
                        if (self.toast) {
                            self.toast.classList.remove('cts-toast--active');
                        }
                    }, timeToHide);
                };

                this.flash = () => {
                    this.show();
                    this.hide();
                };
            };

        return new Toaster();
    }();

    window.Toaster.flash();

//////////////
//end toast
//////////////

    //setup before functions
    var typingTimer;                //timer identifier
    var doneTypingInterval = 200;  //time in ms (.5 seconds)
    var nodeSpinner;

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie) {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie =cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //on keyup, start the countdown
    startTypingTimer = function(node){
        clearTimeout(typingTimer);
        nodeSpinner = $('#spinner_' + getTagboxData(node, 'name'));
        nodeSpinner.removeClass('hidden');
        window.typingTimer = setTimeout(doneTyping, doneTypingInterval, node);
    };

    var getHostnameSuffix = function () {
        return window.location.hostname.includes('qipr.ctsi.ufl.edu') ? '/approver' : '';
    };

    //user is "finished typing," do something
    function doneTyping (node) {
        //do something
        var suffix = getHostnameSuffix();
        $.ajax({
            url: window.location.protocol + '//' + window.location.hostname + suffix + '/api/tags',
            type: 'post',
            data: {"tagString": node.value,
                   "model_name": getTagboxData(node, 'model'),
                   "filter_field": getTagboxData(node, 'filter_field'),
                   "exclude_tags": getSelectedTags(getTagboxData(node, 'name'))},
            success: function(data) {
                jnode = $(node);
                optionList = $('#' + jnode.attr('data-list'));
                optionList.empty();
                $.each(data, function( i, l ){
                    optionList.append($("<li>" + l.display + "</li>")
                                      .attr("value", l)
                                      .mousedown(function() {
                                          var tagProp = l.tag_prop,
                                              model_name = l.model_name;
                                          node.value = $(this).text();
                                          addTag(node, {tagProp:tagProp, model_name:model_name});
                                          $(this).remove();
                                      }));
                });
                optionList.show();
                nodeSpinner.addClass('hidden');
            },
            failure: function(data) {
                console.log("There was an error with the AJAX request");
            }
        });
    }

    // Close the dropdown menu if the user clicks outside of it
    $(document).click( function(event) {
        if (!event.target.matches('dropdown')) {
            closeDropDowns();
        }
    });

    function closeDropDowns() {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = $(dropdowns[i]);
            if (openDropdown.is(":visible") ) {
                openDropdown.hide();
            }
        }
    };

    $(document).on("keypress", ":input:not(textarea)", function(event) {
        return event.keyCode != 13;
    });

    tagboxInputs = document.getElementsByClassName("tagbox__input");

    Array.prototype.forEach.call(tagboxInputs, (node) => {
        node.addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode == 13) {
                addTag(this);
                closeDropDowns();
            }
        });
        node.addEventListener("blur", function(event) {
            closeDropDowns();
        });
        node.addEventListener("input", function(event) {
            var invisibleSpace = '\u200B';
            if (event.target.value.includes(invisibleSpace)){
                addTag(this);
            }
            startTypingTimer(node);
            return true;
        });
    });

    /*
     This function takes a node and a "data-" style attribute
     and returns the value associated with it.
     */
    getTagboxData = function (node, dataNameAttr) {
        if (node.parentElement) {
            if (node.hasAttribute('data-' + dataNameAttr)) {
                return node.getAttribute('data-' + dataNameAttr);
            } else {
                return getTagboxData(node.parentElement, 'name');
            }
        }
    };

    addTag = function(inputNode, customAttrs) {
        var text = inputNode.value.trim(),
            name = getTagboxData(inputNode, 'name'),
            tagHolderId = 'tag-holder_' + name,
            key;

        if (text) {
            if (addValue(name, text)){
                tag = createtag(text, customAttrs);
                document.getElementById(tagHolderId).appendChild(tag);
                inputNode.value = "";
            }
        }
    };

    tagAlreadyExists = function(valuesArray,val) {
        return (valuesArray.map(removeInvisibleSpace).indexOf(removeInvisibleSpace(val)) != -1);
    };

    removeInvisibleSpace = function(inputString){
        return inputString.replace(/\u200B/g, '');
    };

    createtag = function(text, customAttrs) {
        var container = document.createElement('div'),
            li = document.createElement('li'),
            tagDelete = document.createElement('i'),
            icontext = document.createTextNode('close'),
            keys = Object.keys(customAttrs),
            tagtext = document.createTextNode(text);

        container.appendChild(li);
        container.appendChild(tagDelete);
        li.appendChild(tagtext);
        tagDelete.appendChild(icontext);

        li.classList.add('tag');
        keys.forEach(function (key) {
            li.setAttribute(('data-' + key), customAttrs[key]);
        });
        tagDelete.classList.add('tag__delete');
        container.classList.add('tag__container');

        tagDelete.addEventListener('click', function(event) {
            event.preventDefault();
            deleteTag(event);
        });

        return container;
    };

    addValue = function (name, val) {
        var hiddenInputNode = document.getElementById('tag-input_' + name),
            values = hiddenInputNode.value.split(';');
        if (!tagAlreadyExists(values,val)){
            values.push(val);
            hiddenInputNode.value = values.join(';');
            return true;
        }
        return false;
    };

    getSelectedTags = function(nodeName){
        var hiddenInputNode = document.getElementById('tag-input_' + nodeName);
        return removeInvisibleSpace(hiddenInputNode.value);
    };

    deleteTag = function (event) {
        var removeMe = event.target.parentElement,
            value = event.target.parentElement.children[0].textContent,//the li
            parent = removeMe.parentElement;
        removeValue(getTagboxData(event.target, 'name'), value);
        parent.removeChild(removeMe);
    };

    removeValue = function (name, val) {
        var hiddenInputNode = document.getElementById('tag-input_' + name),
            values = hiddenInputNode.value.split(';');
        values = values.filter((item) => item !== val);
        hiddenInputNode.value = values.join(';');
    };

    delete_tags = document.getElementsByClassName("tag__delete");

    Array.prototype.forEach.call(delete_tags, (node) => {
        node.addEventListener('click', deleteTag);
    });

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

    // if the other option in self classification on the about you form is selected,
    // show a new text box for the customer to write in the other classification
    self_classification = document.getElementById('select-self_classification');
    if(self_classification){
        self_classification.onchange = function(){
            if (this.options[this.selectedIndex].value == "other") {
                other_classification_input = document.getElementById('self_classification_other_div');
                //shrink self classification
                this.parentElement.parentElement.classList.remove('m6');
                this.parentElement.parentElement.classList.add('m3');
                //make the other field show
                other_classification_input.style.display = 'block';
            } else {
                other_classification_input = document.getElementById('self_classification_other_div');
                //enlarge self classification
                this.parentElement.parentElement.classList.remove('m3');
                this.parentElement.parentElement.classList.add('m6');
                //make the other field disappear 
                other_classification_input.style.display = 'none';
            }
        };
    };
}();
