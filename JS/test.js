// const palindrom= str => {
//     str=str.toLowerCase()
//     return str===str.split('').reverse().join('')
//   }
  
//  console.log(palindrom("anna"));

 function shuffle(arr){
	var j, temp;
	for(var i = arr.length - 1; i > 0; i--){
     j = Math.floor(Math.random()*(i-1));
     console.log(j);
		temp = arr[j];
		arr[j] = arr[i];
		arr[i] = temp;
	}
	return arr;
}

arr=[1,2,3,4,5,67,7]

console.log(shuffle(arr))
