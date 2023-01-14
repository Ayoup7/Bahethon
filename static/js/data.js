
const list = document.getElementById('validationCustom05')
const department = document.getElementById('department')


$.ajax({
    type: 'GET',
    url:  '/search-data',
    success: function(response){
        const data = response.data
        data.map(vlaue=>{
            list.innerHTML += `<option value="${vlaue.id}"> ${vlaue.department_name}</option>`
          })
    },
    error: function(error){
    }
})

const specialList = document.getElementById('validationCustom04')
department.addEventListener('change', e=>{
    const selected = e.target.value
    specialList.innerHTML = ''
    specialList.innerHTML = `<option selected disabled value="">اختر التخصص الدقيق</option>`
    $.ajax({
        type: 'GET',
        url:  `/get-search-data/${selected}`,
        success: function(response){
            const data = response.data
            if(data.length > 0){
                data.map(vlaues=>{
                    specialList.setAttribute('required', '')
                    specialList.innerHTML += `<option value="${vlaues.id}"> ${vlaues.specialty_name}</option>`
                  })
            }else{
                specialList.removeAttribute('required')
            }
            
        },
        error: function(error){
        }
    })

})


