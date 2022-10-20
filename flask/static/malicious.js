function callServer(url, data, columns, x) {
  $.ajax({
    type: "POST",
    url: url,
    async: false,
    contentType: "application/json",
    data: JSON.stringify({ data: data }),
    dataType: "json",
    success: function (response) {
      columns.push(response.data[x]);
    },
    error: function (err) {
      console.log(err);
    },
  });
  return columns;
}

function PIR(indices, iter, bitarray) {
  var columns = [];
  let x = Math.floor(indices[iter] / Math.sqrt(len));
  let y = Math.sqrt(len) - 1 - (indices[iter] % Math.sqrt(len));

  columns = callServer("/main", bitarray.toString(), columns, x);

  let indexarray = new BitSet();
  indexarray.set(y, 1);

  let final_bitarray = indexarray.xor(bitarray);
  final_bitarray = final_bitarray.toString();

  columns = callServer("/sec", final_bitarray, columns, x);

  var bit = columns[0];
  for (var i = 1; i < columns.length; i++) {
    bit = bit ^ parseInt(columns[i]);
  }
  return bit;
}

async function hashURL(url) {
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
    var bit = await PIR(indices, iter, bitarray);
    malicious_bits.push(bit);
  }
  is_malicious = true;
  for (var i = 0; i < malicious_bits.length; i++) {
    is_malicious = is_malicious & malicious_bits[i];
  }
  if (is_malicious) {
    window.alert("Link is malicious");
  } else {
    window.alert("Link is safe");
  }
  return indices;
}

window.onload = function () {
  var a = document.getElementsByClassName("a");
  for (var i = 0; i < a.length; i++) {
    var url = a[i].href;
    (function (i, url) {
      a[i].addEventListener(
        "click",
        function () {
          hashURL(url);
        },
        false
      );
    })(i, url);
  }
};
