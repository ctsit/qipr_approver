describe('Toaster Test', function () {
    var mockument = document.createDocumentFragment(),
        toastDiv,
        testToaster;
    it('should define window.Toaster', function () {
        expect(window.modules.ToasterFactory).toBeDefined();
        expect(window.Toaster).toBeDefined();
    });

    describe('Toaster instance', function () {
        beforeEach(function () {
            toastDiv = document.createElement('div');
            toastDiv.textContent = 'This comes from django';
            toastDiv.setAttribute('id', 'toast');
            mockument.appendChild(toastDiv);
            window.Toaster.changeDOM(mockument);
            testToaster = window.Toaster;
        });
        it('should have a testToaster.toast dom element', function () {
            expect(testToaster.toast).toBeDefined();
            expect(testToaster.toast).toBe(toastDiv);
        });
        it('should have a show, hide, flash, and changeDOM function', function () {
            expect(typeof testToaster.show).toBe('function');
            expect(typeof testToaster.hide).toBe('function');
            expect(typeof testToaster.flash).toBe('function');
            expect(typeof testToaster.changeDOM).toBe('function');
        });

        describe('methods', function () {
            beforeEach(function () {
                spyOn(testToaster, 'show').and.callThrough();
                spyOn(testToaster, 'hide').and.callThrough();
                spyOn(testToaster, 'flash').and.callThrough();
                spyOn(testToaster, 'changeDOM').and.callThrough();
                testToaster.timeToShow = 0;
                testToaster.timeToHide = 0;
            });
            describe('show', function () {
                it('should add the "cts-toast--active" class to the toaster.toast', function () {
                    testToaster.show();
                    expect(testToaster.toast.classList.contains('cts-toast--active')).toBeTruthy();
                });
            });
            describe('hide', function () {
                it('should remove the "cts-toast--active" class to the toaster.toast', function () {
                    testToaster.hide();
                    expect(testToaster.toast.classList.contains('cts-toast--active')).toBeFalsy();
                });
            });
            describe('flash', function () {
                beforeEach(function (done) {
                    testToaster.flash(done);
                });
                it('should call this.show', function () {
                    expect(testToaster.show).toHaveBeenCalled();
                });
                it('should call this.hide', function () {
                    expect(testToaster.hide).toHaveBeenCalled();
                });
            });
            describe('changeDOM', function () {
                var pseudoDOM,
                    fakeToast = {};
                beforeEach(function () {
                    pseudoDOM = document.createDocumentFragment();
                    spyOn(pseudoDOM, 'getElementById').and.returnValue(fakeToast);
                    testToaster.changeDOM(pseudoDOM);
                });
                afterEach(function () {
                    testToaster.changeDOM(mockument);
                });
                it('should call getElementById with "toast" on the dom object passed', function () {
                    expect(pseudoDOM.getElementById).toHaveBeenCalledWith('toast');
                });
                it('should assign the dom.getElementById return value to this.toast', function () {
                    expect(testToaster.toast).toBe(fakeToast);
                });
            });
        });
    });
});
