var app = new Vue({
    el: '#appProduct',
    data: {
      products: [],
      product: '',
      product_detail: [],
      isActive: false
    },
    methods: {
      onProduct: function (product_id){
        this.isActive = true
        axios.get('/api/v1/products/' + product_id).then(response => {
            console.log(response)
//          добавление в product_detail детализации товара полученного из response data
            this.product_detail = response.data
            console.log(this.product_detail)
          })
      },
      addToCart: function (product_id) {
//          сохранение в переменной токена авторизации полученного из localStorage
            const token = localStorage.getItem('AUTH_TOKEN')
//          отправка пост запроса с данными username и password из формы
          axios.post('/api/v1/cart-products/', {
                headers: {
                    Authorization: "Token " + token
                },
                'product': product_id
            }).then((response) => {

            console.log(response)

          }).catch(function(error) {
                console.log(error)
                alert(error)
            })
      }
    },
    mounted() {
//        сохранение в переменной токена авторизации полученного из localStorage
          const token = localStorage.getItem('AUTH_TOKEN')

          axios.get('/api/v1/products/', {
            headers: {
                Authorization: "Token " + token
            }
            }).then(response => {
            console.log(response)
//          добавление в products списка товаров полученного из response data results
            this.products = response.data.results
            console.log(this.products)
          })
     }
})