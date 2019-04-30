function EnteredNumberOfUseCases(){
  //alert('Linked Successfully!');
  var numberOfUseCases = document.getElementById("NoOfUseCases").value;
  //alert('count is '+numberOfUseCases);
  
  for(let i=0;i<numberOfUseCases;i++){
    var inputtag = document.createElement('input');
    inputtag.setAttribute("type", "file");
    var ids = "id"+ i.toString(10);
    inputtag.setAttribute("id",ids);
    document.body.appendChild(inputtag);
    var br1 = document.createElement('br');
    var br2 = document.createElement('br');
    document.body.appendChild(br1);
    document.body.appendChild(br2);
  }

  // document.getElementById("submit").addEventListener('click',function(){
  //   //alert('I am clicked!');
  //   //console.log('I am here!');

  //   //for(let i=0;i<numberOfUseCases;i++){
  //   //  let ids = "id" + i.toString(10);
  //   //  console.log(document.getElementById(ids));
  //   //  console.log(document.getElementById(ids).files[0].name);
  //   //}


  // });
}