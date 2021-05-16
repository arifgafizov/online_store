var app = new Vue({
    el: '#app',
    data: {
      todos: [
        { text: 'Apple' },
        { text: 'Grape' },
        { text: 'Peach' }
      ],
      username: '',
      password: '',
      isAuthenticated: true
    },
    methods: {
        onSubmit: function () {
            axios.post('/api/v1/users/auth/login/', {
                'username': this.username,
                'password': this.password,
            }).then((response) => {
                console.log(response)
                const token = response.data.token
                localStorage.setItem('AUTH_TOKEN', token)
                this.isAuthenticated = true
            }).catch(function(error) {
                console.log(error)
                alert(error)
            })
        }
    },
    created() {
     const token = localStorage.getItem('AUTH_TOKEN')
     axios.get('/api/v1/users/auth/current/', {
        headers: {
          Authorization: "Token " + token
          }
     })
       .then(({data}) => {
          console.debug(data)
          this.isAuthenticated = true
          this.checkAuthLoading = false
       }).catch((err) => {
          if (err.response?.status === 401) {

            this.isAuthenticated = false


          } else {
        }
      })
     }
})