// $(document).ready(function() {
						   
// 	var hash = window.location.hash.substr(1);
// 	var href = $('#submenu li a').each(function(){
// 		var href = $(this).attr('href');
// 		if(hash==href.substr(0,href.length-5)){
// 			var toLoad = hash+'.html #content';
// 			$('#content').load(toLoad)
// 		}											
// 	});

// 	$('#submenu li a').click(function(){
								  
// 		var toLoad = $(this).attr('href')+' #content';
// 		$('#content').hide('fast',loadContent);
// 		$('#load').remove();
// 		$('#wrapper').append('<span id="load">LOADING...</span>');
// 		$('#load').fadeIn('normal');
// 		window.location.hash = $(this).attr('href').substr(0,$(this).attr('href').length-5);
// 		function loadContent() {
// 			$('#content').load(toLoad,'',showNewContent())
// 		}
// 		function showNewContent() {
// 			$('#content').show('normal',hideLoader());
// 		}
// 		function hideLoader() {
// 			$('#load').fadeOut('normal');
// 		}
// 		return false;
		
// 	});

// });
// window.onload = function () {
//     $('.submenu li a').on('click', function (event) {
//         // alert(event.name)
//         // console.log(event.target.value);
//         var t_href = event.target;
        
//         $.ajax({
//             url: event.target,
            
//             success: function (data) {
//                 // alert(data)
//                 // console.log(data);
//                 $('.content2').html(data, '.content');
//             }
//         });

//         event.preventDefault();
//     });   
// }
// "newArticle.html #articleBody" $('#content').load('pages/page1.php #content');

// window.onload = function () {
//     // console.log('555');
//     $("#list-menu #qwe").on("click", function(event){
//         console.log(event);
//         // alert('66678')
//     });
// }