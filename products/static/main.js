var app = new Vue({
    el: '#app',
    data: {
      todos: [
            { text: 'Foo1' },
            { text: 'Bar1' }
          ],
      products: [],
      username: '',
      password: '',
      isAuthenticated: true,
      isActive: false
    },
    methods: {
        onSubmit: function () {
//          отправка пост запроса с данными username и password из формы
            axios.post('/api/v1/users/auth/login/', {
                'username': this.username,
                'password': this.password,
            }).then ((response) => {
                console.log(response)
//              сохранение в переменной токена авторизации полученного из response data
                const token = response.data.token
//              добавление токена авторизации в localStorage с ключом AUTH_TOKEN
                localStorage.setItem('AUTH_TOKEN', token)
                this.isAuthenticated = true
            }).catch(function(error) {
                console.log(error)
                alert(error)
            })
        },
      inProduct: function (){
        this.isActive = true
      }
    },
    created() {
//    сохранение в переменной токена авторизации полученного из localStorage
     const token = localStorage.getItem('AUTH_TOKEN')
//     отправка гет запроса в заголовке которого токен авторизации
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
     },
     mounted() {
          axios.get('/api/v1/products/').then(response => {
            console.log(response)
//          добавление в products списка товаров полученного из response data results
//            this.products = response.data.results
            this.products.push(response.data.results)
            console.log(this.products)
          })
     }
})