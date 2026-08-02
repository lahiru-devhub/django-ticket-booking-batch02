document.addEventListener("DOMContentLoaded", function(){

    const button = document.getElementById("btn");

    button.addEventListener("click", function(){

        document.getElementById("title").innerHTML =
        "Button Clicked!";

    });

});