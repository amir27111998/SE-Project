 $(document).ready(function(){





    //Hide full analyzer block
    $("#analyzerBlock").css({display:'none'});
    $("#known").css({display:'none'});
    $("#unknown").css({display:'none'});
    //Image field change erroe hide
    $("#img_data").change(function(){
      $('#img_err').text("");
    });

    //loading icon is hidden
    $("#uploading").css({display:'none'});
    var res="";//response global variable
    var progress=0;//progress bar value
    //analyze button
    $("#upload").click(function(){
    //image file can't be empty
      if ($("#img_data").val()!=""){
       var ImageData=$("#img_data")[0].files[0];
      var size=(ImageData.size/1024)/1024;//size of a file

      //condition for size
      if(size>=4)
      {
         $('#img_err').text("Video size should be less than 4 MB");
         return;
      }

      $(this).attr('disabled',"true");  //button will be locked
      $("#uploading").css({display:'block'});//uploading icon will be enabled

      var image=new FormData();
      image.append("image",ImageData);
      console.log("Ajax");

      //POST image file

       $.ajax({
        type: 'POST',
        url: '/dashboard/analyzer',
        processData: false,
        contentType: false,
        data:image,
        success: function (response) {
            if(response){
            console.log(response);
                  $("#uploading").css({display:'none'});//uploading icon will be disabled
                  $("#states").text("Video Uploaded"); //States change
                  res=response;//getting file name
                  $("#analyzerBlock").css({display:'block'});//enable analyzer block but not known and unknown

                  //Updating Progress Bar
                  for(var i=0;i<=20;i++){
                      setTimeout(function(){
                          $("#progress").css({width:progress+'%'});
                          progress++;
                          },800);
                   }

                //Getting the image name
                  $.ajax({
                      type:"GET",
                      url:'/dashboard/capture?name='+res,
                      success:function(response){
                          if(response){
                            //Updating Status
                            $("#states").text("Frames Captured");

                            var data=JSON.parse(response); //Response data image frames
                            //append each frame to slider
                            var divLoc=$("#frames");
                            $.each(data,function(ind,value){
                                var active=''
                                if(ind==0){active='active'}
                                var elem="<div class='carousel-item "+active+" '><img style='height:500px' src='static/images/frames/"+value+"' class='d-block w-100'></div>";
                                divLoc.append(elem);

                            });

                            //update progress
                            for(var i=0;i<=20;i++){
                                setTimeout(function(){
                                    $("#progress").css({width:progress+'%'});
                                    progress++;
                                    },800);
                             }




                             //Getting Matching Faces

                             $.ajax({
                                url:'/dashboard/compare',
                                type:'GET',
                                success:function(response){
                                    var data=JSON.parse(response);
                                    var persons=data;
                                    $("#known").css({display:'block'});
                                    var parent=$("#profile");
                                    //for each loop
                                    if(response!='{}'){
                                    $("#states").text("Recognized Faces");
                                    $.each(data,function(ind,value){
                                    var elem=`<div class='col-xl-3 col-lg-4 col-md-10 col-sm-6 mb-3'>
                                      <div class='card text-muted' style='box-shadow: 0px 2px 17px 0px rgba(0,0,0,0.75);'>
                                        <div class='card-body'>
                                        <img class='card-img-top img-fluid' src='static/images/peoples/`+value[0]+`.jpg' />
                                        </div>
                                        <div class='card-footer'>
                                          <center>
                                          <p class='text-dark'>`+value[1]+`</p>
                                          <a href='/peopleProfile?id=`+value[0]+`' class='btn btn-outline-primary'>View Profile</a>
                                            </center>
                                        </div>

                                      </div>

                                    </div>`;

                                    parent.append(elem);
                                    });}

                                    else{
                                        $("#states").text("No Faces Detected");
                                        var elem=`<div class='col-12'>
                                        <div class='card card-body'>
                                        <p class='text-center text-danger display-4'>No Records Found</p>
                                        </div>
                                        </div>
                                        `;
                                        parent.append(elem);
                                    }

                                    //update progress
                                    for(var i=0;i<=20;i++){
                                        setTimeout(function(){
                                            $("#progress").css({width:progress+'%'});
                                            progress++;
                                            },800);
                                     }


                                    //Getting the unkowns
                                        $.ajax({
                                            url:'/dashboard/unknown',
                                            type:'GET',
                                            success:function(response){
                                                var data=JSON.parse(response);
                                                var unknown=data;
                                                $("#unknown").css({'display':'block'});
                                                var unPro=$("#unknownProfile");
                                                if(data.result.length>0){
                                                $("#states").text("Unknowns Collected");
                                                $.each(data.result,function(ind,value){
                                                    var elem=`<div class='col-xl-3 col-lg-4 col-md-10 col-sm-6 mb-3'>
                                                                  <div class='card text-muted' style='box-shadow: 0px 2px 17px 0px rgba(0,0,0,0.75);'>
                                                                    <div class='card-body'>
                                                                    <img class='card-img-top img-fluid' src='static/images/faces/`+value+`' />
                                                                    </div>
                                                                    <div class='card-footer'>
                                                                      <center>
                                                                      <p class='text-dark'>Unknown</p>
                                                                        </center>
                                                                    </div>

                                                                  </div>

                                                                </div>`;
                                                        unPro.append(elem);


                                                });

                                                }else{
                                                $("#states").text("No Unknowns Found");
                                                var elem=`<div class='col-12'>
                                                        <div class='card card-body'>
                                                        <p class='text-center text-danger display-4'>No Records Found</p>
                                                        </div>
                                                        </div>`;
                                                unPro.append(elem);
                                                }

                                            //update progress
                                    for(var i=0;i<=20;i++){
                                        setTimeout(function(){
                                            $("#progress").css({width:progress+'%'});
                                            progress++;
                                            },800);
                                     }


                                      //PDFS CREATION

                                      var Postdata=new FormData();
                                      Postdata.append("person",JSON.stringify(persons));
                                      Postdata.append("unknown",JSON.stringify(unknown));

                                      $.ajax({
                                            type:'POST',
                                            url:'/dashboard/pdf',
                                            processData: false,
                                            contentType: false,
                                            data:Postdata,
                                            success:function(response){
                                                var link=document.createElement('a');
                                                link.href='/static/pdfs/report.pdf';
                                                link.download="report.pdf";
                                                $("#states").text("Generating Reports");
                                                  for(var i=0;i<=20;i++){
                                                    setTimeout(function(){
                                                        if (progress<=89){
                                                        $("#states").text("Completed");
                                                        }
                                                        $("#progress").css({width:progress+'%'});
                                                        progress++;
                                                        },800);
                                                 }
                                                link.click();

                                            },
                                            error:function(err){
                                                console.log(err);
                                            },
                                            });


                                      //PDFS END




                                            },
                                            error:function(err){
                                                console.log(err);
                                            }
                                        });
                                    //End



                                },
                                error:function(err){
                                    console.log(err);
                                }
                             });






                             //ending Matching Faces

                          }

                      },
                      error:function(err){
                          console.log(err);
                      }
                  });

                //End Get Frames









            };
        },
        error: function (err) {
            console.log(err);
        }
    });





    }
    else{
        //video not selected error
      $('#img_err').text("Please select a video");
    }
    });





  });