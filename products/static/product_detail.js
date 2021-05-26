var app = new Vue({
    el: '#appProductDetail',
    data: {
      title: '',
      description: '',
      price: '',
      weight: '',
      isActive: true
    },
    methods: {
      addToCart: function (product_id) {
//          сохранение в переменной токена авторизации полученного из localStorage
            const token = localStorage.getItem('AUTH_TOKEN')
//          отправка пост запроса с данными username и password из формы
          axios.post('/api/v1/cart-products/', {
                'product': product_id
            },
                {
                    headers: {
                        Authorization: "Token " + token
                    },
                }
            ).then((response) => {

            console.log(response)

          }).catch(function(error) {
                console.log(error)
                alert(error)
            })
      }
    },
    created() {
          const id = location.pathname.split('/').pop()
          axios.get('/api/v1/products/' + id
            ).then(response => {
            console.log(response)
//          добавление в products списка товаров полученного из response data results
            this.title = response.data.title
            this.description = response.data.description
            this.price = response.data.price
            this.weight = response.data.weight || 'вес не определен'
//            if (response.data.weight) {
//                    this.weight = response.data.weight
//                } else {
//                    this.weight = 'вес не определен'
//                }
          }).catch((err) => {
          if (err.response?.status === 404) {
            this.isActive = false
          } else {
            alert(err.response.status +" "+ err.response.statusText)
        }
      })
     },

})