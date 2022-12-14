var dates = document.getElementsByName('dates');
var exercises = document.getElementsByName('exercises');
var numberReps = document.getElementsByName('numberReps');
var numberSets = document.getElementsByName('numberSets');
var repsPerSet = document.getElementsByName('repsPerSet');
var dates_array = [];
for(var i = 0;i < dates.length;i++){
    let v = String(dates[i].value)
    v = v.replace('/','')
    dates_array.push(v)
}
var numberReps_array = [];
for(var i = 0;i < numberReps.length;i++){
    let v = numberReps[i].value
    v = v.replace('/','')
    v = parseInt(v)
    numberReps_array.push(v)
}
var numberSets_array = [];
for(var i = 0;i < numberSets.length;i++){
    let v = numberSets[i].value
    v = v.replace('/','')
    v = parseInt(v)
    numberSets_array.push(v)
}
var repsPerSet_array = [];
for(var i = 0;i < repsPerSet.length;i++){
    let v = repsPerSet[i].value
    v = v.replace('/','')
    v = parseInt(v)
    repsPerSet_array.push(v)
}
const ctx = document.getElementById('myChart');
new Chart(ctx, {
    type: 'bar',
    data: {
    labels: dates_array,
    datasets: [{
        label: '# of reps',
        data: numberReps_array,
        borderWidth: 1,
        borderColor: '#FF6384',
        backgroundColor: '#FFB1C1',
    },
    {
        label: '# of sets',
        data: numberSets_array,
        borderWidth: 1,
        borderColor: '#87CEFA',
        backgroundColor: '#87CEFA',
    },
    {
        label: 'res per set',
        data: repsPerSet_array,
        borderWidth: 1,
        borderColor: '#7FFFD4',
        backgroundColor: '#7FFFD4',
    }
    ]
    },
    options: {
    scales: {
        y: {
            beginAtZero: true
        }
    }
    }
});
const ctx3 = document.getElementById('line_chart');
new Chart(ctx3, {
    type: 'line',
    data: {
    labels: dates_array,
    datasets: [{
        label: '# of reps',
        data: numberReps_array,
        borderWidth: 1,
        borderColor: '#DDA0DD',
        backgroundColor: '#DDA0DD',
    },
    {
        label: '# of sets',
        data: numberSets_array,
        borderWidth: 1,
        borderColor: '#87CEFA',
        backgroundColor: '#87CEFA',
    }
    ]
    },
    options: {
    scales: {
        y: {
            beginAtZero: true
        }
    }
    }
});


var numberB = document.getElementById('numberB').value.replace('/','');
var numberS = document.getElementById('numberS').value.replace('/','');
console.log(numberB)
const ctx2 = document.getElementById('pie_chart');
var myDoughnutChart = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        datasets: [{
            data: [numberB, numberS]
        }],
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Bench Press',
            'Squat'
        ]
    }
});