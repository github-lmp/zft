$(document).ready(function(){
		$("#retrieve_object_submit").click(function(){
			alert("click retrieve_object_submit");	
			var tmp = new Array(2);
			var i = 0;
			$("#retrieve_object_div input:lt(2)").each(function(){
				tmp[i] = $(this).val();
				i++ ;
				alert(tmp);
				});
			$.post("/retrieve_object", 
				{"ccont_name":tmp[0], "filename":tmp[1]},
				function(data){
					alert(data);
					var request = new XMLHttpRequest();
					request.setRequestHeader("X-Auth-Token", data.X-Auth-Token);
					request.open("GET", data.url, true);
					request.send(null);
					alert(request.status);
				},
				"json"
				);
			});
});


