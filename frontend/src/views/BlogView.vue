<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import DailyHots from '@/components/DailyHots.vue'
import { RouterLink } from 'vue-router'

const mediaList = ref([])
const currentPage = ref(1)
const pageSize = 10

axios.get('/api/news').then(res => {
    mediaList.value = res.data.data
})

const totalPages = computed(() => {
    return Math.ceil(mediaList.value.length / pageSize)
})

const currentPageData = computed(() => {
    const startIndex = (currentPage.value - 1) * pageSize
    const endIndex = startIndex + pageSize
    return mediaList.value.slice(startIndex, endIndex)
})

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++
    }
}

const prevPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--
    }
}
</script>

<template>
    <div class="page">
        <div class="container">
            <div class="row">
                <div class="col-md-8">
                    <div class="media" v-for="media in currentPageData" :key="media.id">
                        <div class="media-left">
                            <RouterLink :to="`/news/${ media.id }`" class="media-object-href">
                                <img class="media-object" v-if="media.image_url" :src="media.image_url" />
                            </RouterLink>
                        </div>
                        <div class="media-body">
                            <h4 class="media-heading">{{ media.title }}</h4>
                            {{ media.content }}（访问量：{{ media.view_count }}，发布日期：{{ media.publish_date }}）
                        </div>
                    </div>
                    
                    <ul class="pagination">
                        <li :class="{'disabled': currentPage === 1}">
                            <a href="#" @click.prevent="prevPage" aria-label="Previous">
                                <span aria-hidden="true">«</span>
                            </a>
                        </li>
                        
                        <li v-for="page in totalPages" :key="page" :class="{'active': currentPage === page}">
                            <a href="#" class="page-link" @click.prevent="currentPage = page">{{ page }}</a>
                        </li>

                        <li :class="{'disabled': currentPage === totalPages}">
                            <a href="#" @click.prevent="nextPage" aria-label="Next">
                                <span aria-hidden="true">»</span>
                            </a>
                        </li>
                    </ul>
                </div>
                
                <DailyHots />
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.media-object-href {
    display: block;
    width: 64px;
    height: 64px;
    background: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/PjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ibm9uZSI+PCEtLQpTb3VyY2UgVVJMOiBob2xkZXIuanMvNjR4NjQKQ3JlYXRlZCB3aXRoIEhvbGRlci5qcyAyLjYuMC4KTGVhcm4gbW9yZSBhdCBodHRwOi8vaG9sZGVyanMuY29tCihjKSAyMDEyLTIwMTUgSXZhbiBNYWxvcGluc2t5IC0gaHR0cDovL2ltc2t5LmNvCi0tPjxkZWZzPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+PCFbQ0RBVEFbI2hvbGRlcl8xOTNmNzVkZjVjNiB0ZXh0IHsgZmlsbDojQUFBQUFBO2ZvbnQtd2VpZ2h0OmJvbGQ7Zm9udC1mYW1pbHk6QXJpYWwsIEhlbHZldGljYSwgT3BlbiBTYW5zLCBzYW5zLXNlcmlmLCBtb25vc3BhY2U7Zm9udC1zaXplOjEwcHQgfSBdXT48L3N0eWxlPjwvZGVmcz48ZyBpZD0iaG9sZGVyXzE5M2Y3NWRmNWM2Ij48cmVjdCB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIGZpbGw9IiNFRUVFRUUiLz48Zz48dGV4dCB4PSIxMy40NTgzMzIwNjE3Njc1NzgiIHk9IjM2LjQwMDAwMDA5NTM2NzQzIj42NHg2NDwvdGV4dD48L2c+PC9nPjwvc3ZnPg==);
}

.media-object {
    width: inherit;
    height: inherit;
}
</style>
