from django import forms 

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=20, initial=1,
                                  widget = forms.NumberInput(attrs={'class': 'form-control'}))#widget делает поле красивым с помощбю бутстрапа, attrs для html стилизации
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)#Если override фолз то добавл к тукущ колву, если тру то изм текущ колво на новое, Это скрытое поле (widget=forms.HiddenInput), которое нужно для логики корзины
