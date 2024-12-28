<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const selectedFile = ref(null)
const fileInput = ref(null)
const fileList = ref([])

// 处理文件输入变化
const handleFileChange = (event) => {
    selectedFile.value = event.target.files[0];
}

// 文件上传
const uploadFile = async () => {
    if (!selectedFile.value) {
        alert("请选择一个文件上传！");
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile.value);

    try {
        const response = await axios.post('/api/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        if (response.data.status === 'success') {
            alert('文件上传成功');
            loadFileList();

            selectedFile.value = null;
            if (fileInput.value) {
                fileInput.value.value = '';
            }
        } else {
            alert('文件上传失败');
        }
    } catch (error) {
        console.error("上传文件失败", error);
        alert('上传失败，请稍后再试');
    }
}

// 格式化文件大小（字节 -> KB/MB）
const formatFileSize = (size) => {
    if (size < 1024) return size + ' B';
    else if (size < 1048576) return (size / 1024).toFixed(2) + ' KB';
    else return (size / 1048576).toFixed(2) + ' MB';
}

// 判断文件类型是否为图片
const isImage = (type) => type === 'jpg' || type === 'png' || type === 'gif' || type === 'ico';

// 加载已上传文件列表
const loadFileList = async () => {
    try {
        const response = await axios.get('/api/upload/list');
        fileList.value = response.data.data;
    } catch (error) {
        console.error("加载文件列表失败", error);
    }
}

// 删除文件
const deleteFile = async (fileId) => {
    try {
        const response = await axios.delete(`/api/upload/${fileId}`);
        if (response.data.status === 'success') {
            alert('文件删除成功');
            loadFileList();
        } else {
            alert('文件删除失败');
        }
    } catch (error) {
        console.error("删除文件失败", error);
        alert('删除失败，请稍后再试');
    }
}

// 下载文件
const downloadFile = (fileName) => {
    const link = document.createElement('a');
    link.href = `/upload/${fileName}`;
    link.download = fileName;
    link.click();
}

// 在组件挂载时加载已上传文件列表
onMounted(() => {
    loadFileList();
})
</script>

<template>
    <div class="page">
        <div class="container">
            <h2 class="text-center page-title">文件上传</h2>

            <!-- 文件上传表单 -->
            <div class="row file-upload">
                <div class="col-md-6 col-md-offset-3">
                    <form @submit.prevent="uploadFile">
                        <div class="form-group">
                            <label for="fileInput">选择文件</label>
                            <input type="file" id="fileInput" class="form-control" @change="handleFileChange" ref="fileInput" />
                        </div>
                        <button type="submit" class="btn btn-primary btn-block">上传文件</button>
                    </form>
                </div>
            </div>

            <!-- 文件列表 -->
            <div class="row mt-5 file-list">
                <div class="col-md-6 col-md-offset-3">
                    <h2 class="upload-title">已上传文件</h2>
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>文件名</th>
                                <th>文件大小</th>
                                <th>文件类型</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="fileList.length === 0">
                                <td colspan="4" class="text-center">当前没有上传文件</td>
                            </tr>
                            <tr v-for="(file, index) in fileList" :key="index">
                                <td>
                                    <div class="image-preview" v-if="isImage(file.file_type)">
                                        <div class="image">
                                            <img :src="`/upload/${file.stored_filename}`" width="100" />
                                        </div>
                                        {{ file.original_filename }}
                                    </div>
                                    <div v-else>
                                        {{ file.original_filename }}
                                    </div>
                                </td>
                                <td>{{ formatFileSize(file.size) }}</td>
                                <td>{{ file.file_type }}</td>
                                <td class="operation">
                                    <button class="btn btn-info" @click="downloadFile(file.stored_filename)">下载</button>
                                    <button class="btn btn-danger" @click="deleteFile(file.id)">删除</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.page {
    padding-top: 50px;
}

.page-title {
    margin-bottom: 3rem;
}

.image-preview {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;

    img {
        display: block;
        max-width: 100px;
        height: 50px;
        object-fit: contain;
    }
}

.table th,
.table td {
    text-align: center;
    vertical-align: middle;
}

img {
    border-radius: 5px;
    max-width: 100%;
    height: auto;
}

label, .upload-title {
    font-size: 14px;
    max-width: 100%;
    margin-bottom: 5px;
    font-weight: 700;
}

.operation {
    button {
        padding: 2px 10px;
        margin-right: 0.5rem;

        &:last-child {
            margin-right: 0;
        }
    }
}
</style>