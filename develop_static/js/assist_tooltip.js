const assist_tooltip = {
    "main": main,
}
export default assist_tooltip;
async function main(){
    const AssistCheck = document.getElementById("assist-check");
        let tooltipTriggerList;
        let tooltipList;
        AssistCheck.addEventListener("change", function(){
            if (AssistCheck.checked){
                tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
                tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
                console.log("assisted");
            }else{
                tooltipList.forEach(tooltip => tooltip.dispose());
                console.log("not assisted");
            }
        })
        const assets = await import("/static/assets/tooltip_desc.js");
        const InputList = document.getElementsByClassName("form-control");
        for (let i = 0; i < InputList.length; i++) {
            InputList[i].setAttribute('data-bs-toggle', 'tooltip');
            InputList[i].setAttribute('data-bs-placement', 'top');
            InputList[i].setAttribute('data-bs-title',assets.desc[InputList[i].name]);
        }
    }
    