import numpy as np
from sklearn.datasets import load_iris
"""仅用于加载鸢尾花数据"""

class KMeans:
    """K-means 聚类算法实现"""
    def __init__(self, n_clusters=5, max_iter=300,tol=1e-4,init='random',random_state=None):
        self.n_clusters = n_clusters  # 簇的数量
        self.max_iter = max_iter  # 单次运行最大迭代次数
        self.tol = tol  # 两次迭代之间聚类中心变化的最小容忍度（基于欧氏距离平方和）
        self.init = init  # 初始化办法(记忆/手动输入)
        self.random_state = random_state  # 随机种子，能复现结果
        self.culster_centers_=None  # 存储最后质心
        self.inertia_ = None  # 簇内平方和
        self.n_iter_ = 0  # 存储模型实际迭代次数（计数器）

    def _check_init_centers(self,X):
        """根据init参数初始化聚类中心"""
        n_samples, n_features = X.shape  # 样本数量，每个样本维度
        if isinstance(self.init, np.ndarray):
            if self.init.shape != (self.n_clusters, n_features):
                raise ValueError('init shape error')
            centers = self.init.copy()
        elif self.init == 'random':
            rng = np.random.RandomState(self.random_state)
            # 从样本中随机选取 n_clusters 个不同的样本作为初始中心
            idx = rng.choice(n_samples, size=self.n_clusters, replace=False)
            centers = X[idx].copy()
        else:
            raise ValueError('init type error')
        return centers

    def fit(self,X):
        """训练K——means模型"""
        X= np.array(X)
        n_samples, n_features = X.shape
        # 初始化中心点
        centers = self._check_init_centers(X)
        # 记录样本到最近中心点的距离平方（计算self.inertia）
        labels = np.zeros(n_samples, dtype=int)
        distances = np.zeros(n_samples)

        for i in range(self.max_iter):
            # 1.分配样本到最近中心
            # 利用广播计算每个样本点到每个中心的欧式距离平方和
            dist_matrix = np.sum((X[:, np.newaxis, :] - centers[np.newaxis, :, :]) ** 2, axis=2)
            new_labels = np.argmin(dist_matrix, axis=1)
            new_distances = np.min(dist_matrix, axis=1)

            # 2.检测中心变化是否小于容忍度
            # 计算新中心：按簇取均值
            new_centers = np.zeros_like(centers)
            new_centers = np.zeros_like(centers)
            for k in range(self.n_clusters):
                mask = (new_labels == k)
                if np.any(mask):
                    new_centers[k] = X[mask].mean(axis=0)
                else:
                    # 如果某个簇没有样本，重新随机选择一个样本作为中心
                    rng = np.random.RandomState(self.random_state)
                    idx = rng.choice(n_samples)
                    new_centers[k] = X[idx].copy()
                    # 重新计算一次距离（因为可能出现了空簇）
                    dist_matrix = np.sum((X[:, np.newaxis, :] - new_centers[np.newaxis, :, :]) ** 2, axis=2)
                    new_labels = np.argmin(dist_matrix, axis=1)
                    new_distances = np.min(dist_matrix, axis=1)
            # 重新计算一次距离（因为可能出现了空簇）
            dist_matrix = np.sum((X[:, np.newaxis, :] - new_centers[np.newaxis, :, :]) ** 2, axis=2)
            new_labels = np.argmin(dist_matrix, axis=1)
            new_distances = np.min(dist_matrix, axis=1)
            # 计算中心变化量（欧氏距离平方和）
            center_shift = np.sum((centers - new_centers) ** 2)
            # 更新
            centers = new_centers
            labels = new_labels
            distances = new_distances

            if center_shift < self.tol:
                break

        self.cluster_centers_ = centers
        self.inertia_ = np.sum(distances)
        self.n_iter_ = i + 1
        return self

    def predict(self,X):
        X = np.array(X)
        dist_matrix = np.sum((X[:, np.newaxis, :] - self.cluster_centers_[np.newaxis, :, :]) ** 2, axis=2)
        return np.argmin(dist_matrix, axis=1)

    def fit_predict(self, X): # 降低用户操作成本
        """训练并返回簇标签"""
        self.fit(X)
        return self.predict(X)

"""数据准备"""
iris = load_iris()
X,y_true = iris.data, iris.target

# 标准化
mean = X.mean(axis=0)
std = X.std(axis=0)
X_std = (X - mean) / std


"""模型训练"""
# 随机种子使得结果可复现
kmeans = KMeans(n_clusters=3, max_iter=300, tol=1e-4, init='random', random_state=42)
y_pred = kmeans.fit_predict(X_std)

"""模型评价与分析"""
# 计算纯度
def purity(y_true, y_pred):
    contingency_matrix = np.zeros((3,3))  # 3类鸢尾花
    for i in range(3):  # 真实类别
        for j in range(3):  # 预测簇
            contingency_matrix[i,j] = np.sum((y_true==i) & (y_pred==j))
    # 每个簇取最大值
    return np.sum(np.max(contingency_matrix, axis=0)) / len(y_true)

purity_score = purity(y_true, y_pred)
print(f"纯度: {purity_score:.4f}")
