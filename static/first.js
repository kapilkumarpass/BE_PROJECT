$(window).on('load', function () {
    // let videoclosebtn=document.createElement("button");
    // var para = document.createTextNode('video off');
    // videoclosebtn.appendChild(para);
    // videoclosebtn.style.display='block'
    // videoclosebtn.style.margin='1rem auto'
    // videoclosebtn.type = 'submit';
    // // videoclosebtn.style.backgroundColor='blue'
    // // videoclosebtn.classList.add("btn btn-primary");
    // videoclosebtn.classList.add('btn');
    // videoclosebtn.classList.add('btn-primary');
    // document.getElementsByTagName('body')[0].appendChild(videoclosebtn);
    // videoclosebtn.addEventListener('click',video_off)
    video_off();
  $("#coverScreen").hide();
  });
window.onbeforeunload=()=>{
 
}
// $(document).ready( function() {

 
//     alert("You clicked the button using JQuery!");

// });

// document.getElementById("wait").innerHTML = "Turning on. . . . .";
// setTimeout(showText, 3000);

 



// function showText(){
//   document.getElementById("wait").innerHTML = "Done";
// }

// function opencamera() {

    // im.src=`${window.location.origin}/home/emotion_detector`
  
    

// }
function video_off() {
 setTimeout(()=>{
  // console.log("video closed")
  document.getElementById("demo").src = "";
  // window.location.replace("http://localhost:8000/home/get_songs");
  fetch('http://localhost:8000/home/end_streaming').then(res=>res.text()).then(res=>{
    document.open();
    document.write(res);
    document.close();
  })
  },5000)
  
  // document.getElementById("wait").innerHTML = "Turned off";

}