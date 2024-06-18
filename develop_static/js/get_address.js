function init(event){
    document.addEventListener("DOMContentLoaded", (event) => {
        const radios = document.querySelectorAll(
          'input[type=radio][name="address"]'
        );
        radios.forEach((radio) => {
          radio.addEventListener("change", (event) => {
            if (event.target.checked) {
              let address =
                event.target.nextElementSibling.querySelector("#address").value;
              window.opener.document.getElementById("id_place").value = address;
            }
          });
        });
      });
}
const get_address = {
    "init": init,
}
export default get_address;