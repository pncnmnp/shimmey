function hashURL(url) {
    var malicious_bits = [];
    var indices = [];
    const { hostname } = new URL(url);
    for (var j = 0; j < k; j++) {
        indices.push(murmurHash3.x86.hash32(hostname, offsets[j]) % len);
    }
    let bitarray = new BitSet.Random(Math.sqrt(len));
    while (true) {
        bitarray = new BitSet.Random(Math.sqrt(len));
        if (bitarray.toString().length == Math.sqrt(len)) {
            break;
        }
    }
    for (var iter = 0; iter < k; iter++) {
        var columns = [];
        let x = Math.floor(indices[iter] / Math.sqrt(len));
        let y = (Math.sqrt(len) - 1) - (indices[iter] % Math.sqrt(len));
        $.ajax({
            type: 'POST',
            url: '/main',
            async: false,
            contentType: "application/json",
            data: JSON.stringify({ data: bitarray.toString() }),
            dataType: "json",
            success: function (response) {
                columns.push(response.data[x]);
            },
            error: function (err) {
                console.log(err);
            }
        });
        let indexarray = new BitSet;
        indexarray.set(y, 1);

        let final_bitarray = indexarray.xor(bitarray);
        final_bitarray = final_bitarray.toString();
        // window.alert(final_bitarray + " : " + bitarray.toString());
        $.ajax({
            type: 'POST',
            url: '/sec',
            async: false,
            contentType: "application/json",
            data: JSON.stringify({ data: final_bitarray }),
            dataType: "json",
            success: function (response) {
                columns.push(response.data[x]);
            },
            error: function (err) {
                console.log(err);
            }
        });
        var bit = columns[0];
        for (var i = 1; i < columns.length; i++) {
            bit = bit ^ parseInt(columns[i]);
        }
        malicious_bits.push(bit);
    }
    is_malicious = true;
    for (var i = 0; i < malicious_bits.length; i++) {
        is_malicious = is_malicious & malicious_bits[i];
    }
    if (is_malicious) {
        window.alert("Link is malicious");
    }
    else {
        window.alert("Link is safe");
    }
    return indices;
}

window.onload = function () {
    var a = document.getElementsByClassName("a");
    for (var i = 0; i < a.length; i++) {
        var url = a[i].href;
        (function (i, url) {
            a[i].addEventListener('click', function () { hashURL(url); }, false);
        })(i, url);
    }
}
