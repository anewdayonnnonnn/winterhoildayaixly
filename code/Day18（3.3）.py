import numpy as np
import pandas as pd
import warnings
import os

# 屏蔽无关警告
warnings.filterwarnings('ignore')


# =======1. 线性回归模型类======
class LinearRegression:
    def __init__(self, fit_intercept=True, normalize=False):
        self.fit_intercept = fit_intercept
        self.normalize = normalize
        self.coef_ = None  # 模型系数
        self.intercept_ = None  # 模型截距项
        self.norm_mean = None  # 训练集特征均值（标准化用）
        self.norm_std_ = None  # 训练集特征标准差（标准化用）

    # 内部辅助函数：添加截距列
    def _add_intercept(self, X):
        return np.c_[np.ones(X.shape[0]), X]

    # 内部辅助函数：标准化特征
    def _normalize(self, X, fit=True):
        if fit:
            self.norm_mean = np.mean(X, axis=0)
            self.norm_std_ = np.std(X, axis=0, ddof=1)  # 样本标准差
            self.norm_std_[self.norm_std_ == 0] = 1.0  # 避免除以0
        return (X - self.norm_mean) / self.norm_std_

    # 模型训练核心方法
    def fit(self, X, y, method='normal', lr=0.01, epochs=1000, tol=1e-6):
        X = np.array(X, dtype=np.float64)
        y = np.array(y, dtype=np.float64).flatten()
        n_samples, n_features = X.shape

        # 基础校验
        if n_samples == 0:
            raise ValueError("训练集样本数为0，请检查数据！")
        if len(y) != n_samples:
            raise ValueError(f"特征数({n_samples})与标签数({len(y)})不匹配！")

        # 数据预处理
        if self.normalize:
            X = self._normalize(X, fit=True)
        if self.fit_intercept:
            X = self._add_intercept(X)

        # 参数求解
        if method == 'normal':
            # 正规方程：theta = (X^T X)^-1 X^T y（用伪逆保证稳定性）
            theta = np.linalg.pinv(X.T @ X) @ X.T @ y
        elif method == 'gradient':
            # 梯度下降
            theta = np.zeros(X.shape[1])
            for epoch in range(epochs):
                y_pred = X @ theta
                gradient = (2 / n_samples) * X.T @ (y_pred - y)
                theta_new = theta - lr * gradient
                # 收敛判断
                if np.linalg.norm(theta_new - theta) < tol:
                    theta = theta_new
                    break
                theta = theta_new
        else:
            raise ValueError("method只能是 'normal' 或 'gradient'")

        # 解析系数和截距
        if self.fit_intercept:
            self.intercept_ = theta[0]
            self.coef_ = theta[1:]
        else:
            self.coef_ = theta
            self.intercept_ = 0.0

        return self

    # 预测方法
    def predict(self, X):
        X = np.array(X, dtype=np.float64)
        if self.normalize:
            X = self._normalize(X, fit=False)
        if self.fit_intercept:
            X = self._add_intercept(X)
        theta = np.r_[self.intercept_, self.coef_] if self.fit_intercept else self.coef_
        return X @ theta

    # 计算R²评分
    def score(self, X, y):
        y_pred = self.predict(X)
        y_true = np.array(y, dtype=np.float64).flatten()
        ss_res = np.sum((y_true - y_pred) ** 2)  # 残差平方和
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)  # 总平方和
        return 1 - ss_res / ss_tot if ss_tot != 0 else 0.0


# =======2. 数据读取与预处理======
def load_and_preprocess_data(file_name='housecost.csv'):

    # 1. 查找文件（优先当前目录，再找data子目录）
    possible_paths = [
        file_name,
        os.path.join('data', file_name),
        os.path.join('../data', file_name)
    ]
    file_path = None
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            file_path = abs_path
            break

    if not file_path:
        raise FileNotFoundError(
            f"未找到文件！尝试的路径：{[os.path.abspath(p) for p in possible_paths]}"
        )
    print(f"✅ 找到文件：{file_path}")

    # 2. 尝试多种编码读取CSV（解决中文/特殊字符问题）
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            print(f"✅ 使用编码 {enc} 成功读取数据")
            break
        except Exception as e:
            continue

    if df is None:
        raise ValueError("所有编码都无法读取文件，请检查文件格式！")

    # 3. 数据基本信息展示（调试用）
    print(f"\n 数据基本信息：")
    print(f"原始数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print("\n数据类型信息：")
    print(df.dtypes)
    print("\n前5行数据：")
    print(df.head())

    # 4. 核心修复：处理非数值列和类型转换
    # 4.1 识别并处理非数值列
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    non_numeric_cols = [col for col in df.columns if col not in numeric_cols]

    if non_numeric_cols:
        print(f"\n  发现非数值列：{non_numeric_cols}，将自动删除这些列")
        df = df[numeric_cols]  # 只保留数值列

    if len(df.columns) == 0:
        raise ValueError("数据中没有数值列，无法进行线性回归！")

    # 4.2 强制转换为浮点型并处理无法转换的值
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # 无法转换的设为NaN

    # 4.3 缺失值填充（用列均值）
    print("\n缺失值统计（处理前）：")
    missing_stats = df.isnull().sum()
    print(missing_stats[missing_stats > 0])

    df_filled = df.copy()
    for col in df_filled.columns:
        mean_val = df_filled[col].mean()
        df_filled[col] = df_filled[col].fillna(mean_val)

    # 5. 分离特征和标签（最后一列作为标签）
    X = df_filled.iloc[:, :-1].values  # 所有行，除最后一列
    y = df_filled.iloc[:, -1].values  # 所有行，最后一列
    feature_names = list(df_filled.columns[:-1])
    target_name = df_filled.columns[-1]

    # 6. 最终校验（修复isnan报错的核心）
    # 先转换为float64，再检查缺失值
    X = np.array(X, dtype=np.float64)
    y = np.array(y, dtype=np.float64)

    # 安全检查缺失值
    X_has_nan = np.isnan(X).any()
    y_has_nan = np.isnan(y).any()

    if X_has_nan or y_has_nan:
        # 兜底填充
        X = np.nan_to_num(X, nan=np.nanmean(X))
        y = np.nan_to_num(y, nan=np.nanmean(y))
        print("\n 发现残留缺失值，已自动兜底填充")

    print(f"\n数据预处理完成")
    print(f"特征数: {len(feature_names)}, 标签名: {target_name}")
    print(f"特征形状: {X.shape}, 标签形状: {y.shape}")
    print(f"特征数据类型: {X.dtype}, 标签数据类型: {y.dtype}")

    return X, y, feature_names, target_name


# =======3. 数据集划分======
def split_dataset(X, y, test_size=0.2, random_state=42):
    """划分训练集和测试集"""
    np.random.seed(random_state)
    indices = np.random.permutation(len(X))
    split_idx = int(len(X) * (1 - test_size))
    train_idx, test_idx = indices[:split_idx], indices[split_idx:]

    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    print(f"\n数据集划分完成：")
    print(f"训练集: {X_train.shape[0]} 样本, 测试集: {X_test.shape[0]} 样本")
    return X_train, X_test, y_train, y_test


# =======4. 主程序执行======
if __name__ == "__main__":
    try:
        # 1. 读取数据
        X, y, feature_names, target_name = load_and_preprocess_data('housecost.csv')

        # 2. 划分数据集
        X_train, X_test, y_train, y_test = split_dataset(X, y)

        # 3. 模型训练与评估
        print("\n" + "=" * 80)
        print("模型训练与评估")
        print("=" * 80)

        # 模型1：解析解（无标准化）
        model1 = LinearRegression(fit_intercept=True, normalize=False)
        model1.fit(X_train, y_train, method='normal')
        train_r2_1 = model1.score(X_train, y_train)
        test_r2_1 = model1.score(X_test, y_test)
        print(f"\n【模型1】解析解（无标准化）")
        print(f"截距: {model1.intercept_:.4f}")
        print("前5个特征系数：")
        for i in range(min(5, len(feature_names))):
            print(f"  {feature_names[i]}: {model1.coef_[i]:.4f}")
        print(f"训练集R²: {train_r2_1:.4f}, 测试集R²: {test_r2_1:.4f}")

        # 模型2：解析解（有标准化）
        model2 = LinearRegression(fit_intercept=True, normalize=True)
        model2.fit(X_train, y_train, method='normal')
        train_r2_2 = model2.score(X_train, y_train)
        test_r2_2 = model2.score(X_test, y_test)
        print(f"\n【模型2】解析解（有标准化）")
        print(f"截距: {model2.intercept_:.4f}")
        print("前5个特征系数（标准化后）：")
        for i in range(min(5, len(feature_names))):
            print(f"  {feature_names[i]}: {model2.coef_[i]:.4f}")
        print(f"训练集R²: {train_r2_2:.4f}, 测试集R²: {test_r2_2:.4f}")

        # 模型3：梯度下降（有标准化）
        model3 = LinearRegression(fit_intercept=True, normalize=True)
        model3.fit(X_train, y_train, method='gradient', lr=0.01, epochs=2000)
        train_r2_3 = model3.score(X_train, y_train)
        test_r2_3 = model3.score(X_test, y_test)
        print(f"\n【模型3】梯度下降（有标准化）")
        print(f"截距: {model3.intercept_:.4f}")
        print("前5个特征系数：")
        for i in range(min(5, len(feature_names))):
            print(f"  {feature_names[i]}: {model3.coef_[i]:.4f}")
        print(f"训练集R²: {train_r2_3:.4f}, 测试集R²: {test_r2_3:.4f}")

        # 系数对比
        print("\n" + "=" * 80)
        print("解析解 vs 梯度下降 系数对比")
        print("=" * 80)
        print(f"{'特征名':<15} {'解析解系数':<15} {'梯度下降系数':<15} {'差值':<10}")
        for i, name in enumerate(feature_names):
            diff = model2.coef_[i] - model3.coef_[i]
            print(f"{name:<15} {model2.coef_[i]:<15.4f} {model3.coef_[i]:<15.4f} {diff:<10.2e}")

    except Exception as e:
        print(f"\n 程序执行出错：{type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()  # 打印完整的错误栈，方便调试