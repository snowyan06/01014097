<script setup>
    import { useLayout } from '@/layout/composables/layout';
    import { onBeforeMount, ref } from 'vue';
    import { useRoute } from 'vue-router';

    const route = useRoute();

    const { layoutState, setActiveMenuItem, onMenuToggle } = useLayout();  // 解构出 setActiveMenuItem

    const props = defineProps({
        item: {
            type: Object,
            default: () => ({})
        },
        index: {
            type: Number,
            default: 0
        },
        root: {
            type: Boolean,
            default: true
        },
        parentItemKey: {
            type: String,
            default: null
        }
    });

    const isActiveMenu = ref(false);  // 用于控制当前菜单项的展开状态
    const itemKey = ref(null);

    onBeforeMount(() => {
        itemKey.value = props.parentItemKey ? props.parentItemKey + '-' + props.index : String(props.index);
    });

    function itemClick(event, item) {
        if (item.disabled) {
            event.preventDefault();
            return;
        }

        // 移动端点击时自动关闭菜单
        if ((item.to || item.url) && (layoutState.staticMenuMobileActive || layoutState.overlayMenuActive)) {
            onMenuToggle();
        }

        if (item.command) {
            item.command({ originalEvent: event, item: item });
        }

        // 如果有子菜单，则切换当前菜单的展开状态
        if (item.items) {
            isActiveMenu.value = !isActiveMenu.value;  // 立即展开或收回
        }

        // 使用 setActiveMenuItem 方法更新当前激活的菜单项
        const foundItemKey = item.items ? (isActiveMenu.value ? props.parentItemKey : itemKey) : itemKey.value;
        setActiveMenuItem(foundItemKey);  // 使用 setActiveMenuItem 来更新
    }

    function checkActiveRoute(item) {
        return route.path === item.to;
    }
</script>

<template>
    <li :class="{ 'layout-root-menuitem': root, 'active-menuitem': isActiveMenu }">
        <div v-if="root && item.visible !== false" class="layout-menuitem-root-text">{{ item.label }}</div>
        <a v-if="(!item.to || item.items) && item.visible !== false" :href="item.url" @click="itemClick($event, item, index)" :class="item.class" :target="item.target" tabindex="0">
            <i :class="item.icon" class="layout-menuitem-icon"></i>
            <span class="layout-menuitem-text">{{ item.label }}</span>
            <i class="pi pi-fw pi-angle-down layout-submenu-toggler" v-if="item.items"></i>
        </a>
        <router-link v-if="item.to && !item.items && item.visible !== false" @click="itemClick($event, item, index)" :class="[item.class, { 'active-route': checkActiveRoute(item) }]" tabindex="0" :to="item.to">
            <i :class="item.icon" class="layout-menuitem-icon"></i>
            <span class="layout-menuitem-text">{{ item.label }}</span>
            <i class="pi pi-fw pi-angle-down layout-submenu-toggler" v-if="item.items"></i>
        </router-link>
        <Transition v-if="item.items && item.visible !== false" name="layout-submenu">
            <ul v-show="root ? true : isActiveMenu" class="layout-submenu">
                <app-menu-item v-for="(child, i) in item.items" :key="child" :index="i" :item="child" :parentItemKey="itemKey" :root="false"></app-menu-item>
            </ul>
        </Transition>
    </li>
</template>

<style lang="scss" scoped></style>
