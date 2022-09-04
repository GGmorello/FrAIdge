// const dropArea = document.querySelector('.drag-area');
// const dragText = document.querySelector('.header');

// let button = dropArea.querySelector('.button');
// let input = dropArea.querySelector('input');
// let submit = dropArea.querySelector('submit');

// let file;

// button.onclick = () => {
//   input.click();
// };

// // when browse
// input.addEventListener('change', function () {
//   file = this.files[0];
//   dropArea.classList.add('active');
//   displayFile();
// });

// // when file is inside drag area
// dropArea.addEventListener('dragover', (event) => {
//   event.preventDefault();
//   dropArea.classList.add('active');
//   dragText.textContent = 'Release to Upload';
//   // console.log('File is inside the drag area');
// });

// // when file leave the drag area
// dropArea.addEventListener('dragleave', () => {
//   dropArea.classList.remove('active');
//   // console.log('File left the drag area');
//   dragText.textContent = 'Drag & Drop';
// });

// // when file is dropped
// dropArea.addEventListener('drop', (event) => {
//   event.preventDefault();
//   // console.log('File is dropped in drag area');

//   var fileList = event.dataTransfer.files;
//   // console.log(file);

//   // var xhr = new XMLHttpRequest();
//   // console.log('test');
//   // console.log(xhr);

//   // xhr.open('post', '/upload', true); // aussume that the url /upload handles uploading.
  
//   // // send files to server
//   // xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
//   // var fd = new FormData();
//   // for (let file of fileList) {
//   //     fd.append('files', file);
//   // }
//   // xhr.send(fd);

//   file = event.dataTransfer.files[0];
//   let formData = new FormData();
     
//   formData.append("file", file);
//   fetch('', {method: "POST", body: formData});

//   // const ctrl = new AbortController()    // timeout
//   //   setTimeout(() => ctrl.abort(), 5000);
    
//   //   try {
//   //      let r = await fetch('/upload/image', 
//   //        {method: "POST", body: formData, signal: ctrl.signal}); 
//   //      console.log('HTTP response code:',r.status); 
//   //   } catch(e) {
//   //      console.log('Huston we have problem...:', e);
//     // }
//   // document.getElementById("image-form").submit();
//   // displayFile();

// });

// function displayFile() {
//   let fileType = file.type;
//   // console.log(fileType);

//   let validExtensions = ['image/jpeg', 'image/jpg', 'image/png'];

//   if (validExtensions.includes(fileType)) {
//     // console.log('This is an image file');
//     let fileReader = new FileReader();

//     fileReader.onload = () => {
//       let fileURL = fileReader.result;
//       // console.log(fileURL);
//       let imgTag = `<img src="${fileURL}" alt="">`;
//       dropArea.innerHTML = imgTag;
//     };
//     fileReader.readAsDataURL(file);
//   } else {
//     alert('This is not an Image File');
//     dropArea.classList.remove('active');
//   }
// }

// // async function SavePhoto(inp) 
// // {
// //   let user = { name:'john', age:34 };
// //   let formData = new FormData();
// //   let photo = inp.files[0];      
       
// //   formData.append("photo", photo);
// //   formData.append("user", JSON.stringify(user)); 
  
// //   const ctrl = new AbortController()    // timeout
// //   setTimeout(() => ctrl.abort(), 5000);
  
// //   try {
// //     let r = await fetch('/upload/image', 
// //       {method: "POST", body: formData, signal: ctrl.signal}); 
// //     console.log('HTTP response code:',r.status); 
// //   } catch(e) {
// //     console.log('Huston we have problem...:', e);
// //   }
    
// // }
