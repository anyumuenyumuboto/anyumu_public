import polars as pl

@pl.api.register_dataframe_namespace("tvtsplit")
class Shuffle_tvt_split:
    def __init__(
        self,
        df: pl.DataFrame,
    ):
        self._df = df
        self.df_length = df.select(pl.len()).item()

    def train_length(self, params: dict[str : bool | float] = None) -> int:

        if params is None:
            params = {"shuffle": True, "seed": 0, "val_size": 0.25, "test_size": 0.25}

        return (
            self.df_length
            - int(self.df_length * params["val_size"])
            - int(self.df_length * params["test_size"])
        )

    def val_length(self, params: dict[str : bool | float] = None) -> int:

        if params is None:
            params = {"shuffle": True, "seed": 0, "val_size": 0.25, "test_size": 0.25}

        return int(self.df_length * params["val_size"])

    def test_length(self, params: dict[str : bool | float] = None) -> int:

        if params is None:
            params = {"shuffle": True, "seed": 0, "val_size": 0.25, "test_size": 0.25}

        return int(self.df_length * params["test_length"])

    def train(self, params: dict[str : bool | float] = None) -> pl.DataFrame:

        if params is None:
            params = {"shuffle": True, "seed": 0, "val_size": 0.25, "test_size": 0.25}

        df = (
            self._df.select(pl.all().shuffle(seed=params["seed"]))
            if params["shuffle"] == True
            else self._df
        )

        return (
            df.with_row_index(name="n")
            .filter((pl.col("n") >= 0) & (pl.col("n") < self.train_length(params)))
            .drop("n")
        )

    def val(self, params: dict[str : bool | float] = None) -> pl.DataFrame:

        if params is None:
            params = {"shuffle": True, "seed": 0, "val_size": 0.25, "test_size": 0.25}

        df = (
            self._df.select(pl.all().shuffle(seed=params["seed"]))
            if params["shuffle"] == True
            else self._df
        )

        return (
            df.with_row_index(name="n")
            .filter(
                (pl.col("n") >= self.train_length(params))
                & (pl.col("n") < self.train_length(params) + self.val_length(params))
            )
            .drop("n")
        )

    def test(self, params: dict[str : bool | float] = None) -> pl.DataFrame:

        if params is None:
            params = {"shuffle": True, "seed": 0, "val_size": 0.25, "test_size": 0.25}

        df = (
            self._df.select(pl.all().shuffle(seed=params["seed"]))
            if params["shuffle"] == True
            else self._df
        )

        return (
            df.with_row_index(name="n")
            .filter(
                (pl.col("n") >= self.train_length(params) + self.val_length(params))
                & (pl.col("n") < self.df_length)
            )
            .drop("n")
        )

    def tvt(self, params: dict[str : bool | float] = None) -> dict[str : pl.DataFrame]:

        if params is None:
            params = {"shuffle": True, "seed": 0, "val_size": 0.25, "test_size": 0.25}

        return {
            "train": self.train(params),
            "val": self.val(params),
            "test": self.test(params),
        }
    
# def test_TVTsplit():

#     params = {"shuffle": False, "seed": 0, "val_size": 0.25, "test_size": 0.25}
#     sample_df = pl.DataFrame(
#         data=["aaa", "bbb", "ccc", "ddd", "eee", "fff"],
#         schema=[("txt", pl.String)],
#     )

#     print(sample_df.tvt_split.train(params))
#     print(sample_df.tvt_split.val(params))
#     print(sample_df.tvt_split.test(params))

# if __name__ == "__main__":
#     #main()
#     test_TVTsplit()