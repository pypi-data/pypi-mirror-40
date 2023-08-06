def setup():
    from glue.config import menubar_plugin
    from .statistics import StatsGui

    @menubar_plugin("Show Statistics")
    def my_plugin(session, data_collection):
        ex = StatsGui(data_collection)
        ex.show()
        session.ex = ex