// JavaScript Document
   $(function($){  
  setInterval(function(){  
    $(".slideshow ul li:first-child").animate({"margin-left": -350}, 1000, function(){  
        $(this).css("margin-left",0).appendTo(".slideshow ul");  
    });  
  }, 3500);  
});