#%%
import sys
import numpy as np
import pandas as pd
import plotnine
import statsmodels.formula.api as smf

from plotnine import (
    ggplot,
    aes,
    after_stat,
    geom_point,
    geom_histogram,
    geom_boxplot,
    geom_line,
    geom_ribbon,
    stat_smooth,
    stat_density_2d,
    facet_grid,
    facet_wrap,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    scale_fill_cmap,
    coord_fixed,
    coord_cartesian,
    theme,
    theme_gray,
    theme_minimal,
    element_rect,
    element_text,
)

print("Python:", sys.executable)
print("plotnine:", plotnine.__version__)


#%%
# 1. Bộ dữ liệu Palmer Penguins có sẵn trong plotnine.
from plotnine.data import penguins as penguins_raw
penguins = penguins_raw.copy()
penguins.head()

print("Number of rows and columns:", penguins.shape)

print("Variable names:", penguins.columns.tolist())
penguins.columns

print("Xem kiểu dữ liệu")
penguins.info()


# %%  2. Thống kê mô tả
print("Thống kê mô tả cho các biến số học:")
penguins.describe()

# %% Cach phân bố của các biến định tính
print("Phân bố của species:")
penguins["species"].value_counts()

print("Phân bố của sex:")
penguins["sex"].value_counts(dropna=False)

# %% Kiêm trả missing
print("Kiểm tra missing values:")   
penguins.isnull().sum()

print("Lọc dữ liệu không có giá trị thiếu:")   
penguins_complete = penguins.dropna().copy()
print("Số lượng hàng sau khi lọc:", penguins_complete.shape)

# %% Đồ thị
(
    ggplot(
        penguins,
        aes(
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
        ),
    )
    + labs(title="Palmer Penguins")
)


(
    ggplot(
        penguins,
        aes(
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
        ),
    )
    + labs(title="Palmer Penguins")
)


# %% 3. Các loại đồ thị
(
    ggplot(
        penguins_complete,
        aes(
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
            shape="sex",
        ),
    )
    + geom_point(size=3)
    + labs(
        title="Bill length vs Bill depth",
        x="Bill length (mm)",
        y="Bill depth (mm)",
        color="Species",
        size="Body mass (g)",
        shape="Sex",
    )
)

# %% 4. Mapping size to body mass

aes(color="species")
(
    ggplot(
        penguins,
        aes(
            x="flipper_length_mm",
            y="body_mass_g",
            color="species",
        ),
    )
    + geom_point()
    + labs(
        title="Color được ánh xạ vào species",
        x="Flipper length (mm)",
        y="Body mass (g)",
        color="Species",
    )
)

# %% 5. HISTOGRAM

(
    ggplot(
        penguins,
        aes(x="body_mass_g"),
    )
    + geom_histogram(
        binwidth=250,
        color="white",
    )
    + labs(
        title="Distribution of penguin body mass",
        x="Body mass (g)",
        y="Count",
    )
)

#%%

(
    ggplot(
        penguins,
        aes(x="flipper_length_mm"),
    )
    + geom_histogram(
        binwidth=10,
        color="white",
    )
    + labs(
        title="Distribution of penguin flipper length",
        x="Flipper length (mm)",
        y="Count",
    )
)


# %%  Regression line

(
    ggplot(
        penguins,
        aes(
            x="flipper_length_mm",
            y="body_mass_g",
        ),
    )
    + geom_point(alpha=0.6)
    + stat_smooth(
        method="lm",
        se=True,
        level=0.95,
        color="red",
        fill="pink",
        alpha=0.3,
    )
    + labs(
        title="Body mass vs Flipper length",
        subtitle="Linear regression with 95% confidence interval",
        x="Flipper length (mm)",
        y="Body mass (g)",
    )
    + theme_minimal()
)

# %%

reg_data = (
    penguins[
        ["flipper_length_mm", "body_mass_g"]
    ]
    .dropna()
    .copy()
)

model = smf.ols(
    "body_mass_g ~ flipper_length_mm",
    data=reg_data,
).fit()

prediction_grid = pd.DataFrame(
    {
        "flipper_length_mm": np.linspace(
            reg_data["flipper_length_mm"].min(),
            reg_data["flipper_length_mm"].max(),
            200,
        )
    }
)

prediction = (
    model
    .get_prediction(prediction_grid)
    .summary_frame(alpha=0.05)
)

prediction_grid = pd.concat(
    [
        prediction_grid.reset_index(drop=True),
        prediction.reset_index(drop=True),
    ],
    axis=1,
)

prediction_grid.head()

(
    ggplot()
    + geom_ribbon(
        data=prediction_grid,
        mapping=aes(
            x="flipper_length_mm",
            ymin="obs_ci_lower",
            ymax="obs_ci_upper",
        ),
        fill="lightgray",
        alpha=0.5,
    )
    + geom_ribbon(
        data=prediction_grid,
        mapping=aes(
            x="flipper_length_mm",
            ymin="mean_ci_lower",
            ymax="mean_ci_upper",
        ),
        fill="pink",
        alpha=0.7,
    )
    + geom_point(
        data=reg_data,
        mapping=aes(
            x="flipper_length_mm",
            y="body_mass_g",
        ),
        alpha=0.55,
    )
    + geom_line(
        data=prediction_grid,
        mapping=aes(
            x="flipper_length_mm",
            y="mean",
        ),
        color="red",
        size=1,
    )
    + labs(
        title="Confidence interval vs Prediction interval",
        subtitle=(
            "Pink: 95% CI for mean response; "
            "gray: 95% prediction interval for a new penguin"
        ),
        x="Flipper length (mm)",
        y="Body mass (g)",
    )
    + theme_minimal()
)
# %% 9. Grouping trong statistical layer


(
    ggplot(
        penguins,
        aes(
            x="flipper_length_mm",
            y="body_mass_g",
            color="species",
        ),
    )
    + geom_point(alpha=0.65)
    + stat_smooth(
        method="lm",
        se=False,
    )
    + labs(
        title="Body mass vs Flipper length",
        subtitle="Regression được ước lượng riêng cho từng species",
        x="Flipper length (mm)",
        y="Body mass (g)",
        color="Species",
    )
    + theme_minimal()
)


(
    ggplot(
        penguins,
        aes(
            x="flipper_length_mm",
            y="body_mass_g",
            color="species",
            fill="species",
        ),
    )
    + geom_point(alpha=0.6)
    + stat_smooth(
        method="lm",
        se=True,
        level=0.95,
        alpha=0.18,
    )
    + labs(
        title="Body mass vs Flipper length by species",
        subtitle="Regression lines and 95% confidence bands",
        x="Flipper length (mm)",
        y="Body mass (g)",
        color="Species",
        fill="Species",
    )
    + theme_minimal()
)

# %% 10. Faceting chia dữ liệu thành các subset và tạo một panel cho mỗi subset.

(
    ggplot(
        penguins,
        aes(
            x="flipper_length_mm",
            y="body_mass_g",
        ),
    )
    + geom_point(alpha=0.7)
    + facet_grid(". ~ species")
    + labs(
        title="Body mass vs Flipper length",
        subtitle="Một panel cho mỗi species",
        x="Flipper length (mm)",
        y="Body mass (g)",
    )
)

# %%
(
    ggplot(
        penguins_complete,
        aes(
            x="flipper_length_mm",
            y="body_mass_g",
            color="species",
        ),
    )
    + geom_point()
    + facet_grid("sex ~ .")
    + labs(
        title="Body mass vs Flipper length",
        subtitle="Một hàng cho mỗi sex",
        x="Flipper length (mm)",
        y="Body mass (g)",
        color="Species",
    )
)
# %%
(
    ggplot(
        penguins_complete,
        aes(
            x="flipper_length_mm",
            y="body_mass_g",
        ),
    )
    + geom_point()
    + stat_smooth(
        method="lm",
        se=False,
        color="red",
    )
    + facet_grid("sex ~ species")
    + labs(
        title="Body mass vs Flipper length",
        subtitle="Phân chia đồng thời theo sex và species",
        x="Flipper length (mm)",
        y="Body mass (g)",
    )
)
# %% 15. Boxplot

(
    ggplot(
        penguins,
        aes(
            x="species",
            y="body_mass_g",
            fill="species",
        ),
    )
    + geom_boxplot()
    + labs(
        title="Body mass by species",
        x="Species",
        y="Body mass (g)",
        fill="Species",
    )
    + theme_minimal()
)


#%% 12. Scales
(
    ggplot(
        penguins,
        aes(
            x="flipper_length_mm",
            y="body_mass_g",
            color="species",
        ),
    )
    + geom_point()
    + scale_x_continuous(
        name="Flipper length (mm)",
        breaks=[170, 180, 190, 200, 210, 220, 230],
    )
    + scale_y_continuous(
        name="Body mass (g)",
        breaks=[3000, 4000, 5000, 6000],
    )
    + labs(
        title="Body mass vs Flipper length",
        color="Species",
    )
)

# %% 13. Ghép toàn bộ Grammar of Graphics

(
    ggplot(
        penguins,
        aes(
            x="flipper_length_mm",
            y="body_mass_g",
            color="species",
        ),
    )
    + geom_point(
        size=2,
        alpha=0.65,
    )
    + stat_smooth(
        method="lm",
        se=False,
    )
    + facet_wrap("species")
    + scale_x_continuous(
        breaks=[170, 180, 190, 200, 210, 220, 230],
    )
    + labs(
        title="Body mass and flipper length",
        subtitle="Points, regression, color, facets, scale và theme",
        x="Flipper length (mm)",
        y="Body mass (g)",
        color="Species",
    )
    + theme_minimal()
)
# %% 14. Statistical transformation nâng cao
(
    ggplot(
        penguins,
        aes(
            x="bill_length_mm",
            y="bill_depth_mm",
        ),
    )
    + stat_density_2d(
        aes(fill=after_stat("level")),
        geom="polygon",
        color="white",
    )
    + scale_fill_cmap(
        cmap_name="viridis",
        name="Density",
    )
    + labs(
        title="2D density of bill morphology",
        x="Bill length (mm)",
        y="Bill depth (mm)",
    )
    + theme_minimal()
)
# %%
p_bill_length = (
    ggplot(
        penguins,
        aes(x="bill_length_mm"),
    )
    + geom_histogram(
        binwidth=2,
        color="white",
    )
    + labs(
        title="Bill length",
        x="Bill length (mm)",
        y="Count",
    )
)

p_bill_depth = (
    ggplot(
        penguins,
        aes(x="bill_depth_mm"),
    )
    + geom_histogram(
        binwidth=1,
        color="white",
    )
    + labs(
        title="Bill depth",
        x="Bill depth (mm)",
        y="Count",
    )
)

p_flipper = (
    ggplot(
        penguins,
        aes(x="flipper_length_mm"),
    )
    + geom_histogram(
        binwidth=5,
        color="white",
    )
    + labs(
        title="Flipper length",
        x="Flipper length (mm)",
        y="Count",
    )
)

p_mass = (
    ggplot(
        penguins,
        aes(x="body_mass_g"),
    )
    + geom_histogram(
        binwidth=250,
        color="white",
    )
    + labs(
        title="Body mass",
        x="Body mass (g)",
        y="Count",
    )
)

print("Các biểu đồ riêng lẻ -  Xep Ngang:")
p_bill_length | p_bill_depth


p_bill_length / p_bill_depth

# %%
panel = (
    (p_bill_length | p_bill_depth)
    /
    (p_flipper | p_mass)
)

panel & theme_minimal()

# %%
