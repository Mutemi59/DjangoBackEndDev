const alert_container = document.querySelector(".alert-msg-container")
const close_alert = document.querySelector(".close-alert")
const add_form = document.getElementById("add_form")

setTimeout(() => {
    alert_container.style.visibility = "hidden"
}, 3000);

close_alert.onclick = () =>{

    alert_container.style.visibility = "hidden"
}
