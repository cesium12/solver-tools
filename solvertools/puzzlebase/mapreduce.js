// run this code in the server to make the totals table

m = function () {
    var rel = this.rel;
    var freq = this.freq;
    this.words.forEach(
        function (word) {
            emit(rel+' '+word, {total: freq, rel: rel, word: word});
        }
    );
}

r = function (key, values) {
    var tot = 0;
    for (var i = 0; i < values.length; i++) {
        tot += values[i].total;
    }
    return {total:tot, rel: values[0].rel, word: values[0].word};
}

db.runCommand({mapreduce: 'relations', map: m, reduce: r, out: 'totals'})

