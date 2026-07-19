<template>
    <div class="logout">
        <h2>登出成功</h2>
        <p>您已经成功登出，正在跳转到登录页...</p>
    </div>
</template>

<script>
export default {
    name: 'Logout',
    mounted() {
        // 清除登录状态
        localStorage.removeItem('isLoggedIn');

        // 重定向到登录页面
        this.$router.push({ name: 'login' });
    }
}
</script>

<style scoped>
.logout {
    text-align: center;
    margin-top: 50px;
}

h2 {
    font-size: 24px;
    margin-bottom: 20px;
}

p {
    font-size: 16px;
    color: gray;
}
</style>
