$(document).ready(function () {
		// Settings up the tree - using $(selector).jstree(options);
		// All those configuration options are documented in the _docs folder
		$("#demo")
		.jstree({
				"plugins" : [ "themes", "json_data", "ui", "crrm", "cookies", "dnd", "search", "types", "hotkeys", "contextmenu" ],

				"json_data" : {
				// I chose an ajax enabled tree - again - as this is most common, and maybe a bit more complex
				// All the options are the same as jQuery's except for `data` which CAN (not should) be a function
    				"ajax" : {
    						// the URL to fetch the data
    						"url" : "/demo?demo=demo",
    						// this function is executed in the instance's scope (this refers to the tree instance)
    						// the parameter is the node being loaded (may be -1, 0, or undefined when loading the root nodes)
    						"data" : function (n) {
    								// the result is fed to the AJAX request `data` option
    								return {
    										"operation" : "get_children",
    										"id" : n.attr ? n.attr("id").replace("node_","") : "null_-1_super"
    								};
    						}
    				}
				},

				// Configuring the search plugin
				"search" : {
						// As this has been a common question - async search
						// Same as above - the `ajax` config option is actually jQuery's object (only `data` can be a function)
						"ajax" : {
						"url" : "/demo?demo=demo",
						// You get the search string as a parameter
								"data" : function (str) {
										return {
												"operation" : "search",
												"search_str" : str
										};
									}
							}
					},

					// Using types - most of the time this is an overkill
					// Still meny people use them - here is how
					"types" : {
							// I set both options to -2, as I do not need depth and children count checking
							// Those two checks may slow jstree a lot, so use only when needed
							"max_depth" : -2,
							"max_children" : -2,
							// I want only `drive` nodes to be root nodes
							// This will prevent moving or creating any other type as a root node
							//							"valid_children" : [ "drive" ],
							"types" : {
									// The default type
									"default" : {
											// I want this type to have no children (so only leaf nodes)
											// In my case - those are files
											"valid_children" : "none",
											// If we specify an icon for the default type it WILL OVERRIDE the theme icons
											"icon" : {
													"image" : "/static/img/file.png"
											}
									},
									// The user type
    							"0" : {
    									// I want this type to have no children (so only leaf nodes)
    									// In my case - those are files
    									"valid_children" : "none",
    									// If we specify an icon for the default type it WILL OVERRIDE the theme icons
    									"icon" : {
    												"image" : "/static/img/file.png"
    									}
    							},
									// The `group` type
        					"-1" : {
											// can have files and other folders inside of it, but NOT `drive` nodes
											"valid_children" : ["default", "group", "user" ],
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
													"create group": {
															"label": "Create group",
															"action": function(obj) {
																	//													alert($(obj).html())
																	if ($(obj).attr("id").split("_")[3] != "group"){
																			alert("只能在用户组下面添加组或用户。");
																			return false;
																	}
																	$("#addUserDiv").hide();
																	$("#addGroupDiv").show();
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
													"create user": {
															"label": "Create user",
															"action": function(obj) {
																	//													alert($(obj).html())
																	//													alert($(obj).attr("id"));
																	if ($(obj).attr("id").split("_")[3] != "group"){
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
			})

  	.bind("create.jstree", function (e, data) {
  			$.post("/demo?demo=demo",
  			{
      			"operation" : "create_node",
      			"id" : data.rslt.parent.attr("id").replace("node_",""),
      			"position" : data.rslt.position,
      			"title" : data.rslt.name,
      			"type" : data.rslt.obj.attr("rel")
  			},
  			function (r) {
  					if(r.status) {
  							//alert(r.status);
  							//alert(r.id);
  							$(data.rslt.obj).attr("id", "node_" + r.id);
  					}
  					else {
  							$.jstree.rollback(data.rlbk);
  					}
  			}, "json"
  			);
  	})
  	.bind("remove.jstree", function (e, data) {
  			data.rslt.obj.each(function () {
  					$.ajax({
  							async : false,
                type: 'POST',
                url: "/demo?demo=demo",
                dataType: "json",
                data : {
  									"operation" : "remove_node",
  									"id" : this.id.replace("node_","")
  							},
  							success : function (r) {
  									if(!r.status) {
  											data.inst.refresh();
  									}
  							}
  					});
  			});
  	})
  	.bind("rename.jstree", function (e, data) {
  			$.post("/demo?demo=demo", {
      			"operation" : "rename_node",
      			"id" : data.rslt.obj.attr("id").replace("node_",""),
      			"title" : data.rslt.new_name
  			},
  			function (r) {
  					if(!r.status) {
  							$.jstree.rollback(data.rlbk);
  							alert(r.msg);
  					}
  			}, "json");
  	})
  
  	.bind("move_node.jstree", function (e, data) {
  			data.rslt.o.each(function(i) {
  					$.ajax({
  							async : false,
                type: 'POST',
                url: "/demo?demo=demo",
                dataType: "json",
  							data :{
  									"operation" : "move_node",
                    "id" : $(this).attr("id").replace("node_",""),
                    "ref" : data.rslt.np.attr("id").replace("node_",""),
                    "position" : data.rslt.cp + i,
                    "title" : data.rslt.name,
                    "copy" : data.rslt.cy ? 1 : 0
  							},
      					success : function(r){
          					if(!r.status) {
          							$.jstree.rollback(data.rlbk);
          							alert(r.msg)
          					}
          					else {
          							$(data.rslt.oc).attr("id", "node_" + r.id);
          							if(data.rslt.cy && $(data.rslt.oc).children("UL").length) {
          									data.inst.refresh(data.inst._get_parent(data.rslt.oc));
          							}
          					}
          					$("#analyze").click();
      					}
  					});
  			});
  	});


    //控制上面的一行菜单
    $("#mmenu input").click(function() {
    		switch(this.id) {
    				case "add_default":
        		case "add_group":
        		$("#demo").jstree("create", 
    						$(".jstree-clicked"), "last", { "attr" : { "rel" : this.id.toString().replace("add_","")}}
    				);
        		break;
        		case "search":
    						$("#demo").jstree("search", document.getElementById("text").value);
    						break;
    				case "text": break;
    						default:
    						$("#demo").jstree(this.id);
    						break;
       	}
    });
    
    
    //控制添加group, user.
    var DEBUG = false;
    $("#demo a").livequery("click",function(){
    		if (DEBUG) {alert($(this).parent().html()); }
    		var id = ($(this).parent().attr("id"));
    		if ($(this).parent().attr("rel") == "group"){
    				if (DEBUG) {alert("good, here is group.");	}
    				//首先去掉input的不可编辑状态，值改变后，恢复不可编辑状态。
    				$("#userGroup").removeAttr("readonly");
    				$("#groupGroup").removeAttr("readonly");
    				$(".userInput").each(function(){
    						$(this).val("");
    						//					alert("here userInput.");
    				});
    				$("#userGroup").val(id);
    				$("#groupGroup").val(id);
    				$("#userGroup").attr("readonly", "true");
    				$("#groupGroup").attr("readonly", "true");
    		}
    		//下面这两行首先去掉原来的颜色，在给新选择的元素上色。
    		$(".jstree-clicked").removeClass("jstree-clicked");
    		$(this).addClass("jstree-clicked");
    		return false;
    });
    
    $("#addGroup").click(function() {
    		//获取要添加用户组的信息，保存在group里面。
    		var group = new Array;
    		var i = 0;
    		$("#addGroupDiv input").slice(0, 3).each(function(){
    				group[i] = $(this).val() ;
    				i++;
    		});
    		var groupName = group[0];
    		var groupGroup = group[1];//父节点的id值。
    		var groupPermis = group[2];
    		if (DEBUG){
    				alert(group);
    				alert(groupName + groupGroup + groupPermis);
    		}
    		// 发送待添加组的信息到服务器端。
    		$.post("/demo?demo=demo",
    				{"operation" : "create_node",
    				"position" : "last",
    				"title" : groupName,
    				"type" : "group",
    				"id": groupGroup.replace("node_", ""),
    				"permis": groupPermis,
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
    
    $("#addUser").click(function() {
    		//获取要添加用户组的信息，保存在group里面。
    		var user = new Array;
    		var i = 0;
    		$("#addUserDiv input").slice(0, 4).each(function(){
    				user[i] = $(this).val() ;
    				i++;
    		});
    		var userName = user[0];
    		var userGroup = user[1];//父节点的id值。
    		var userPassword1 = user[2];
    		var userPassword2 = user[3];
    		if ( userPassword1 == "" ){
    				alert("密码不能为空");
    				return false;
    		}
    		if ( userPassword1 != userPassword2 ){
    				alert("两次密码输入的不一样。");
    				return false;
    		}
    		else{
    				var userPassword = userPassword1;
    		}
    		// 发送待添加组的信息到服务器端。
    		$.post(
    				"/demo?demo=demo",
    				{"operation" : "create_node",
    					"position" : "last",
    					"title" : userName,
    					"type" : "user",
    					"id": userGroup.replace("node_", ""),
    					"password": userPassword,
    				},
    				function (r) {
    						if(r.status) {
    								//						alert(r.status);
    								//						alert(r.id);
    								$("#demo").jstree("create", $(".jstree-clicked"), "last", { "data":userName, "attr" : { "rel" : "user", "id":r.id} }, userName);
    								$("#addUserDiv").hide();
    						}
    						else {
    								alert(r.msg);
    						}
    					}, "json");
    });
    
});
