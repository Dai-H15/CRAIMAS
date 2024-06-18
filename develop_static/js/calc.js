const calc = {
    "apply_calc": apply_calc
}

function apply_calc() {
    var capital = document.getElementById("capital");
    var sales = document.getElementById("sales");
    var input1 = document.getElementById("1");
    var input2 = document.getElementById("2");
    var value1 = input1.value;
    var value2 = input2.value;
    var result = Number(value1 * 10000) + Number(value2);
    if (capital.checked) {
      window.opener.document.getElementById("id_capital").value = result;
    } else if (sales.checked) {
      window.opener.document.getElementById("id_sales_n").value = result;
    }
  };
export default calc;