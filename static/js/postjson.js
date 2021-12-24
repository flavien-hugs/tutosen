console.log('load post json data');

const dataBox = document.getElementById('data-box');
const spinnerBox = document.getElementById('spinner-box');


$.ajax({
	type: 'GET',
	url: '/blog/post/json/',
	success: function(response){
		setTimeout(() => {
			spinnerBox.classList.add('d-none')
			for(const item of response){
				dataBox.innerHTML += `${item.title}`
			}
		}, 500)
	},
	error: function(error){
		setTimeout(() => {
			spinnerBox.classList.add('d-none')
			dataBox.innerHTML += `<p class="font-weight-normal">Failed to load the data.</p>`
		}, 500)
	}
})
