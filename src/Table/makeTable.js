//function is set to noop then makes the table only allowing it to be called once
export function makeTable(data) {
  makeTable = nof;
  var table = document.getElementById('myTable')
  let i = 0

  for (let item in data) {
    var row = `<tr>
                 <td>${item}: ${data[item]}</td>
               </tr>`
    table.innerHTML += row
    console.log(i)
    i++
  }
}

//no operation function
function nof() {};
