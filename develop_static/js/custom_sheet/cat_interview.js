const cat_interview = {
    "init": init
}

function init(){
    document.getElementById('choice').addEventListener('change', function() {
        window.location.href = this.value;
    });
}

export default cat_interview;