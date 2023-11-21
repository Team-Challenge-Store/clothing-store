import replace from "gulp-replace"; //Пошук та заміна
import plumber from "gulp-plumber";//обробка помилок
import notify from "gulp-notify";//повідомлення
import browsersync from "browser-sync";//Локальний сервер
import newer from "gulp-newer";//Перевірка оновлень
import gulpIf from "gulp-if";//Умовне розгалуження

//Експорт об'єкту
export const plugins = {
    replace: replace,
    plumber: plumber,
    notify: notify,
    browsersync: browsersync,
    newer: newer,
    if: gulpIf,
}