Vue.filter('jsonIt', function(value) {
    return value;
});
new Vue({
    el: '#wrapper',
    data: {
        tasks: [
            'Body'
        ],
        newURL: '',
        results1: '',
        loading: false,
        submitButtonText: 'Submit',
    },
    methods: {
        getWordCount: function(jobID) {
            var self = this;
            let promise2 = $.ajax({
                url: 'http://10.0.10.32:8000/results/' + jobID,
                //data: JSON.stringify(data),
                type: 'GET',
                //contentType: 'application/json;charset=utf-8',
                //dataType: 'json',
            });

            function handleResults(result, status, xhr) {
                console.log('This is from Count results');
                if(xhr.status == 202) {
                    console.log(result, status + '\t Results from 202');
                } else if (xhr.status == 200) {
                    console.log(result);
                    self.loading = false;
                    self.submitButtonText = 'Submit';
                    self.results1 = result;
                }
            }
            function handleResultsf(result, error) {
                console.log('Result of done is\t' + JSON.stringify(result.responseText) + JSON.stringify(result) + JSON.stringify(error) );
            }
            promise2.then(handleResults, handleResultsf);
            console.log('Results + id over');
        //Results from jobID finished
        },
        getJobId: function(e){
            var self = this;
            e.preventDefault();
            var t = $('form').serialize();
            console.log(t);
            var newURL = this.newTask;
            data = {'url': newURL}
            console.log(newURL);
            let promise1 = $.ajax({
                url: 'http://10.0.10.32:8000/start',
                data: JSON.stringify(data),
                type: 'POST',
                contentType: 'application/json;charset=utf-8',
                dataType: 'text',
            });

            function handleResult(result) {
                console.log('Executing Success!')
                console.log('Result of done is' + result);
                self.getWordCount(result);
                self.submitButtonText = 'Loading....';
                self.loading = true;
                self.results1 = '';
                let tm = setInterval(function() {
                    self.getWordCount(result)
                }, 14000 );
                setTimeout(function() {clearInterval(tm); console.log('Clear Interval stopped'); }, 40000);
            }
            function handleResultf(result, error) {
                console.log('Result of done is\t' + JSON.stringify(result.responseText) + JSON.stringify(result) + JSON.stringify(error) );
            }
            promise1.then(handleResult, handleResultf);
        //Ajax call over and so is that method addTask
        },




        //Methods finish
    },
})
