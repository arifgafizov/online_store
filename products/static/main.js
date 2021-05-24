var app = new Vue({
    el: '#app',
    data: {
      cart_products: [],
      orders: [],
      cart_total_price: '',
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
      onProduct: function (product_id){
        this.isActive = true
        axios.get('/api/v1/products/' + product_id).then(response => {
            console.log(response)
//          добавление в product_detail детализации товара полученного из response data
            this.product_detail = response.data
            console.log(this.product_detail)
          })
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
          this.isActive = true
          //    сохранение в переменной токена авторизации полученного из localStorage
          const token = localStorage.getItem('AUTH_TOKEN')
          //     отправка гет запроса в заголовке которого токен авторизации
//          получение товаров в корзине
          axios.get('/api/v1/cart-products/', {
                headers: {
                    Authorization: "Token " + token
                }
            }).then(response => {

            console.log(response)
//          добавление в cart_products списка товаров корзины полученного из response data
            this.cart_products = response.data
            console.log(this.cart_products)
          }),

//          получение общей цены товаров в корзине
          axios.get('/api/v1/cart-products/cart-total-price/', {
                headers: {
                    Authorization: "Token " + token
                }
            }).then(response => {

            console.log(response)
//          добавление в cart_products списка товаров корзины полученного из response data
            this.cart_total_price = response.data
            console.log(this.cart_total_price)
          }),

//          получение заказа
          axios.get('/api/v1/orders/', {
                headers: {
                    Authorization: "Token " + token
                }
            }).then(response => {

            console.log(response)
//          добавление в orders списка товаров корзины полученного из response data
            this.orders = response.data
            console.log(this.orders)
          })
     }
})