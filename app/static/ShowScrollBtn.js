// кнопки прокрутки появятся только если высота содержимого больше высоты окна

function ShowScrollBtn() {
	if (document.documentElement.scrollHeight > document.documentElement.clientHeight) 
	{
		// block (для встроенных элементов: span, ...)  - показать none - скрыть еще есть inline (как div, p)
		document.getElementById("scrollBtns").style.display = "block"; 
	}

	else 
	{
		document.getElementById("scrollBtns").style.display = "none";
	}
}


// Как правильно реализовать универсальные функции show и hide для DOM элемента? 
// function toggle(el) {
//   el.style.display = (el.style.display == 'none') ? '' : 'none'
// }
// свойство display сбрасывается - при этом элемент получает display из CSS по умолчанию, то есть то, которое было изначально:
// Свойство display у элемента может отличаться от унаследованного из CSS
// Или особое значение display могло быть установлено из javascript.
// При этом обнуление display сбросит это особое значение.

// так будет корректно (2 ф. для момента когда скрываем и показываем эл.):
// function hide(el) {
// 	if (!el.hasAttribute('displayOld')) {
// 		el.setAttribute("displayOld", el.style.display)
// 	}
// 	el.style.display = "none"
// }
// function show(el) {
// 	var old = el.getAttribute("displayOld");
// 	el.style.display = old || "";
// }

// проблема в том, что если эл. спрятан стилем css, js его не покажет
// решение здесь http: javascript.ru/ui/show-hide-toggle


// =========================================

// window - элемент самого высокого уровня

// событие "при прокрутке страницы"
// window.onscroll = function() { ... }

// на сколько рх прокручена страница:
// document.documentElement.scrollTop || window.pageYOffset 

// это можно использовать для подзагрузки контента при прокрутке страницы
// или показа кнопок прокрутки

// =====================

// function confirmDelete() {
//     if (confirm("Вы подтверждаете удаление?")) {
//         return true;
//     } else {
//         return false;
//     }
// }

// <a href="delete_file.php" onclick="return confirmDelete();">Удалить файл</a>

// можно еще проще:
// onclick="return confirm('are u shure?')"

// ====================================

// таймаут

// <input type="button" onclick="on()" value="Запустить таймаут">
// <input type="button" onclick="off()" value="Остановить отсчет">

// <script>
// function go() { alert('Я сработало') }

// function on() {
//     timeoutId = setTimeout(go, 3000)
// }

// function off() {
//     clearTimeout(timeoutId)
// }
// </script>
