
import streamlit as st
from database_workshop import Database

st.set_page_config(
    page_title="Управление продукцией",

    layout="wide"
)



@st.cache_resource
def init_database():
    return Database()


if 'db' not in st.session_state:
    st.session_state.db = init_database()

if 'user' not in st.session_state:
    st.session_state.user = None

st.title(" Управление продукцией компании")

tab1, tab2, tab3, tab4 = st.tabs(["Продукция", "Цеха", "Добавить", "Войти"])

with tab1:
    st.header(" Список продукции")

    # Кнопка обновления
    if st.button("Обновить список"):
        st.rerun()

    products = st.session_state.db.get_products_with_workshops()

    if products:
        for product in products:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(product[1])
                    st.write(f"**Цена:** {product[2]} руб.")
                    st.write(f"**Цех:** {product[3]}")
                with col2:
                    st.write(f"ID: {product[0]}")
    else:
        st.info("Продукция не найдена")


with tab2:
    st.header(" Список цехов")

    workshops = st.session_state.db.get_all_workshops()

    if workshops:
        # Показываем в виде карточек
        cols = st.columns(2)
        for idx, workshop in enumerate(workshops):
            with cols[idx % 2]:
                with st.container(border=True):
                    st.write(f"### {workshop[1]}")
                    st.write(f"ID: {workshop[0]}")
                    if workshop[2]:
                        st.write(f"Описание: {workshop[2]}")
    else:
        st.info("Цеха не найдены")

    st.divider()

    # Форма добавления цеха
    st.subheader("Добавить новый цех")
    with st.form("add_workshop_form", clear_on_submit=True):
        name = st.text_input("Название цеха")
        description = st.text_area("Описание")

        if st.form_submit_button("Добавить цех"):
            if name:
                if st.session_state.db.add_workshop(name, description):
                    st.success(f"Цех '{name}' добавлен!")
                    st.rerun()
                else:
                    st.error("Ошибка при добавлении")
            else:
                st.warning("Введите название цеха")

with tab3:
    st.header("Добавить продукцию")

    workshops = st.session_state.db.get_all_workshops()

    with st.form("add_product_form", clear_on_submit=True):
        name = st.text_input("Название продукции")
        price = st.number_input("Цена (руб.)", min_value=0.0, step=0.01)

        if workshops:
            # Создаем список для выбора
            workshop_list = [f"{ws[0]} - {ws[1]}" for ws in workshops]
            selected = st.selectbox("Выберите цех", workshop_list)
            workshop_id = int(selected.split(" - ")[0])
        else:
            st.warning("Сначала добавьте цех!")
            workshop_id = None

        if st.form_submit_button("Добавить продукт"):
            if name and price > 0:
                if st.session_state.db.add_product(name, price, workshop_id):
                    st.success(f"Продукт '{name}' добавлен!")
                    st.rerun()
                else:
                    st.error("Ошибка при добавлении")
            else:
                st.warning("Заполните все поля")

# === ВКЛАДКА 4: АВТОРИЗАЦИЯ ===
with tab4:
    st.header("Вход в систему")

    if st.session_state.user:
        st.success(f"Вы вошли как: {st.session_state.user[1]}")
        if st.button("Выйти"):
            st.session_state.user = None
            st.rerun()
    else:
        # Форма входа
        with st.form("login_form"):
            username = st.text_input("Имя пользователя")
            password = st.text_input("Пароль", type="password")

            if st.form_submit_button("Войти"):
                user = st.session_state.db.check_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success(f"Добро пожаловать, {username}!")
                    st.rerun()
                else:
                    st.error("Неверные данные")

        st.divider()

        # Форма регистрации
        st.subheader("Регистрация")
        with st.form("register_form"):
            new_user = st.text_input("Новое имя пользователя")
            new_pass = st.text_input("Новый пароль", type="password")

            if st.form_submit_button("Зарегистрироваться"):
                if new_user and new_pass:
                    if st.session_state.db.add_user(new_user, new_pass):
                        st.success("Регистрация успешна! Теперь войдите.")
                    else:
                        st.error("Пользователь уже существует")
                else:
                    st.warning("Заполните все поля")

st.divider()
st.write("Система управления продукцией компании")