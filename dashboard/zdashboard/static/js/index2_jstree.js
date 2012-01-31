$(document).ready(function () {
		$("#demo")
		.jstree({
				"plugins" : [ "themes", "json_data", "ui", "crrm", "cookies", "dnd", "search", "types", "hotkeys", "contextmenu" ],

				"json_data" : {
    				"ajax" : {
    						"url" : "/jstree",
    						"data" : function (n) {
    								return {
    										"operation" : "get_children",
    										"id" : n.attr ? n.attr("id").replace("node_","") : "-1_-1_0"
    								};
    						}
    				}
				},

				// Configuring the search plugin
				"search" : {
						"ajax" : {
						"url" : "/node",
								"data" : function (str) {
										return {
												"operation" : "search",
												"search_str" : str
										};
									}
							}
					},

					"types" : {
							// I set both options to -2, as I do not need depth and children count checking
							// Those two checks may slow jstree a lot, so use only when needed
							"max_depth" : -2,
							"max_children" : -2,
							// I want only `drive` nodes to be root nodes
							// This will prevent moving or creating any other type as a root node
							"valid_children" : ['0'],
							"types" : {
									// The default type
									//"default" : {
											//// I want this type to have no children (so only leaf nodes)
											//// In my case - those are files
											//"valid_children" : "none",
											//// If we specify an icon for the default type it WILL OVERRIDE the theme icons
											//"icon" : {
													//"image" : "/static/img/file.png"
											//}
									//},
									// The user type
    							'1' : {
    									// I want this type to have no children (so only leaf nodes)
    									// In my case - those are files
    									"valid_children" : "none",
    									// If we specify an icon for the default type it WILL OVERRIDE the theme icons
    									"icon" : {
    												"image" : "/static/img/file.png"
    									}
    							},
									// The `group` type
        					"0" : {
											// can have files and other folders inside of it, but NOT `drive` nodes
											"valid_children" : ["-1", "0" ],
											"icon" : {
													"image" : "/static/img/folder.png"
											}
        					},
							}
					},

					// For UI & core - the nodes to initially select and open will be overwritten by the cookie plugin
					"themes": {
							"theme":"apple",
							"url":"/static/css/jstree_themes/themes/apple/style.css",
							"dots": true,
							"icons":true,
					},

					"contextmenu": {
							"items"	: {
									"create": {
											"label": "Create",
											"action": function(obj) {},
											"_disabled"         : false,     // clicking the item won't do a thing
											"_class"            : "class",  // class is applied to the item LI node
											"separator_before"  : false,    // Insert a separator before the item
											"separator_after"   : true,     // Insert a separator after the item
											// false or string - if does not contain `/` - used as classname
											"icon"              : false,
											"submenu"           : {
													/* Collection of objects (the same structure) */
													"create folder": {
															"label": "Create folder",
															"action": function(obj) {
																	alert($(obj).attr('id'));
																	if ($(obj).attr("id").split("_")[3] != "0"){
																			alert("只能在目录下面添加文件或目录。");
																			return false;
																	}
																	$("#addUserDiv").hide();
																	$("#addGroupDiv").show();
																	$(obj).children("a").trigger("click");
															},
                							"_disabled"         : false,     // clicking the item won't do a thing
                							"_class"            : "class",  // class is applied to the item LI node
                							"separator_before"  : false,    // Insert a separator before the item
                							"separator_after"   : true,     // Insert a separator after the item
                							// false or string - if does not contain `/` - used as classname
                							"icon"              : false,
                					},
													"create file": {
															"label": "Create file",
															"action": function(obj) {
																	//													alert($(obj).html())
																	//													alert($(obj).attr("id"));
																	if ($(obj).attr("id").split("_")[3] != "0"){
																			alert("只能在用户组下面添加组或用户。");
																			return false;
																	}
                									$("#addGroupDiv").hide();
                									$("#addUserDiv").show();
                									$(obj).children("a").trigger("click");
                									//													alert("i am here");
															},
                							"_disabled"         : false,     // clicking the item won't do a thing
                							"_class"            : "class",  // class is applied to the item LI node
                							"separator_before"  : false,    // Insert a separator before the item
                							"separator_after"   : true,     // Insert a separator after the item
                							// false or string - if does not contain `/` - used as classname
                							"icon"              : false,
													},
											},
									},

							},
					},

					// the UI plugin - it handles selecting/deselecting/hovering nodes
					"ui" : {
							// this makes the node with ID node_4 selected onload
							"initially_select" : [ "node_4" ]
					},

					// the core plugin - not many options here
					"core" : {
							// just open those two nodes up
							// as this is an AJAX enabled tree, both will be downloaded from the server
							"initially_open" : [ "node_2" , "node_3" ]
					},
			});

    //控制上面的一行菜单
    $("#mmenu input").click(function () {
    		switch(this.id) {
        		case "search":
    						$("#demo").jstree("search", document.getElementById("text").value);
    						break;
    				case "text": 
								break;
    				default:
    						$("#demo").jstree(this.id);
    						break;
       	}
    });
    
    
    //控制添加group, user.
    $("#demo a").livequery("click",function(){
    		var id = ($(this).parent().attr("id"));
				if ($(this).parent().attr("rel") == "0"){
    				//首先去掉input的不可编辑状态，值改变后，恢复不可编辑状态。
    				$("#userGroup").removeAttr("readonly");
    				$("#groupGroup").removeAttr("readonly");
    				$(".userInput").each(function(){
    						$(this).val("");
    				});
    				$("#userGroup").val(id);
    				$("#groupGroup").val(id);
    				$("#userGroup").attr("readonly", "true");
    				$("#groupGroup").attr("readonly", "true");
    		}
				$(".jstree-clicked").removeClass("jstree-clicked");
    		$(this).addClass("jstree-clicked");
    		return false;
    });
    
    $("#addGroup").livequery('click', function(){
    		//获取要添加用户组的信息，保存在group里面。
    		var group = new Array;
    		var i = 0;
				$("#addGroupDiv input").slice(0, 3).each(function(){
    				group[i] = $(this).val() ;
    				i++;
    		});
    		var groupName = group[0];
    		var groupGroup = group[1];//父节点的id值。
    		var tag = group[2];
    		$.post("/jstree",
    				{"operation" : "create_node",
    				"position" : "last",
    				"name" : groupName,
    				"type" : "0",
    				"tag" : tag,
    				"id": groupGroup.replace("node_", ""),
    				},
    				function (r) {
    						if(r.status) {
        						//alert(r.status);
        						//alert(r.id);
        						$("#demo").jstree("create", $(".jstree-clicked"), "last", 
        							{ "data":groupName, "state":"open", "attr" : { "rel" : "group", "id":r.id} }, groupName);
        						$("#addGroupDiv").hide();
    						}
    						else {
    								alert(r.msg);
    						}
    				}, "json");
    		});

		$('#testclick').livequery('click', function(){
				alert('you click me,');
				});
    
    $("#addUser").click(function() {
    		//获取要添加用户组的信息，保存在group里面。
				return false;
    });
    
});
