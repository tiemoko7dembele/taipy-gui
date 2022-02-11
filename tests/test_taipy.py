import datetime
import os
from copyreg import pickle
from time import sleep
from unittest import mock

from pytest import TempdirFactory

from taipy import Taipy
from taipy import Taipy as tp
from taipy.common.alias import JobId, PipelineId, ScenarioId, TaskId
from taipy.common.frequency import Frequency
from taipy.config.config import Config
from taipy.config.data_node_config import DataNodeConfig
from taipy.config.pipeline_config import PipelineConfig
from taipy.config.scenario_config import ScenarioConfig
from taipy.config.task_config import TaskConfig
from taipy.cycle.cycle_manager import CycleManager
from taipy.data.data_manager import DataManager
from taipy.data.pickle import PickleDataNode
from taipy.data.scope import Scope
from taipy.job.job import Job
from taipy.job.job_manager import JobManager
from taipy.pipeline.pipeline_manager import PipelineManager
from taipy.scenario.scenario_manager import ScenarioManager
from taipy.scheduler.scheduler import Scheduler
from taipy.task.task_manager import TaskManager


def file_exists(file_path):
    return os.path.exists(file_path)


def assert_file_exists(file_path):
    assert file_exists(file_path), f"File {file_path} does not exist"


def assert_file_not_exists(file_path):
    assert not file_exists(file_path), f"File {file_path} exists"


class TestTaipy:
    def test_load_configuration(self):
        file_name = "my_file.toml"
        with mock.patch("taipy.config.config.Config.load") as load:
            tp.load_configuration(file_name)
            load.assert_called_once_with(file_name)

    def test_export_configuration(self):
        file_name = "my_file.toml"
        with mock.patch("taipy.config.config.Config.export") as export:
            tp.export_configuration(file_name)
            export.assert_called_once_with(file_name)

    def test_configure_global_app(self):
        a, b, c, d, e, f = "foo", "bar", "baz", "qux", "quux", "grault"
        with mock.patch("taipy.config.config.Config.set_global_config") as set_global:
            tp.configure_global_app(a, b, c, d, e, property=f)
            set_global.assert_called_once_with(a, b, c, d, e, property=f)

    def test_configure_job_executions(self):
        a, b, c, d, e, f, g, h, i = "foo", "bar", "baz", "qux", "quux", "quz", "corge", "grault", "garphy"
        with mock.patch("taipy.config.config.Config.set_job_config") as mck:
            tp.configure_job_executions(a, b, c, d, e, f, g, h, i, my_property=i)
            mck.assert_called_once_with(a, b, c, d, e, f, g, h, i, my_property=i)

    def test_configure_data_node(self):
        a, b, c, d = "foo", "bar", Scope.PIPELINE, "qux"
        with mock.patch("taipy.config.config.Config.add_data_node") as mck:
            tp.configure_data_node(a, b, c, property=d)
            mck.assert_called_once_with(a, b, c, property=d)

    def test_configure_default_data_node(self):
        a, b, c = "foo", Scope.PIPELINE, "qux"
        with mock.patch("taipy.config.config.Config.add_default_data_node") as mck:
            tp.configure_default_data_node(a, b, property=c)
            mck.assert_called_once_with(a, b, property=c)

    def test_configure_task(self):
        a, b, c, d, e, f, g, h = "foo", "bar", "baz", "qux", "quux", "quz", "corge", "grault"
        with mock.patch("taipy.config.config.Config.add_task") as mck:
            tp.configure_task(a, [], b, [], properties={c: d, e: f, g: h})
            mck.assert_called_once_with(a, [], b, [], properties={c: d, e: f, g: h})

    def test_configure_default_task(self):
        c, e, f, g, h = "baz", "quux", "quz", "corge", "grault"
        with mock.patch("taipy.config.config.Config.add_default_task") as mck:
            tp.configure_default_task([], c, [], properties={e: f, g: h})
            mck.assert_called_once_with([], c, [], properties={e: f, g: h})

    def test_configure_pipeline(self):
        a, b, c = "foo", "bar", "baz"
        with mock.patch("taipy.config.config.Config.add_pipeline") as mck:
            tp.configure_pipeline(a, b, my_property=c)
            mck.assert_called_once_with(a, b, my_property=c)

    def test_configure_default_pipeline(self):
        a, b = "foo", "bar"
        with mock.patch("taipy.config.config.Config.add_default_pipeline") as mck:
            tp.configure_default_pipeline(a, my_property=b)
            mck.assert_called_once_with(a, my_property=b)

    def test_configure_scenario(self):
        a, b, c, d, e = "foo", "bar", "baz", "qux", "quux"
        with mock.patch("taipy.config.config.Config.add_scenario") as set_global:
            tp.configure_scenario(a, b, c, d, property=e)
            set_global.assert_called_once_with(a, b, c, d, property=e)

    def test_configure_default_scenario(self):
        a, b, c, d = "foo", "bar", Scope.PIPELINE, "qux"
        with mock.patch("taipy.config.config.Config.add_default_scenario") as mck:
            tp.configure_default_scenario(a, b, c, property=d)
            mck.assert_called_once_with(a, b, c, property=d)

    def test_check_configuration(self):
        with mock.patch("taipy.config.config.Config.check") as mck:
            tp.check_configuration()
            mck.assert_called_once_with()

    def test_set(self, scenario, cycle, pipeline, data_node, task):
        with mock.patch("taipy.data.data_manager.DataManager.set") as mck:
            tp.set(data_node)
            mck.assert_called_once_with(data_node)
        with mock.patch("taipy.task.task_manager.TaskManager.set") as mck:
            tp.set(task)
            mck.assert_called_once_with(task)
        with mock.patch("taipy.pipeline.pipeline_manager.PipelineManager.set") as mck:
            tp.set(pipeline)
            mck.assert_called_once_with(pipeline)
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.set") as mck:
            tp.set(scenario)
            mck.assert_called_once_with(scenario)
        with mock.patch("taipy.cycle.cycle_manager.CycleManager.set") as mck:
            tp.set(cycle)
            mck.assert_called_once_with(cycle)

    def test_submit(self, scenario, pipeline):
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.submit") as mck:
            tp.submit(scenario)
            mck.assert_called_once_with(scenario)
        with mock.patch("taipy.pipeline.pipeline_manager.PipelineManager.submit") as mck:
            tp.submit(pipeline)
            mck.assert_called_once_with(pipeline)

    def test_get_tasks(self):
        with mock.patch("taipy.task.task_manager.TaskManager.get_all") as mck:
            tp.get_tasks()
            mck.assert_called_once_with()

    def test_get_task(self, task):
        with mock.patch("taipy.task.task_manager.TaskManager.get") as mck:
            task_id = TaskId("TASK_id")
            tp.get(task_id)
            mck.assert_called_once_with(task_id)

    def test_delete_scenario(self):
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.hard_delete") as mck:
            scenario_id = ScenarioId("scenario_id")
            tp.delete_scenario(scenario_id)
            mck.assert_called_once_with(scenario_id)

    def test_get_scenarios(self, cycle):
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.get_all") as mck:
            tp.get_scenarios()
            mck.assert_called_once_with()
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.get_all_by_cycle") as mck:
            tp.get_scenarios(cycle)
            mck.assert_called_once_with(cycle)

    def test_get_scenario(self, scenario):
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.get") as mck:
            scenario_id = ScenarioId("SCENARIO_id")
            tp.get(scenario_id)
            mck.assert_called_once_with(scenario_id)

    def test_get_master(self, cycle):
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.get_master") as mck:
            tp.get_master(cycle)
            mck.assert_called_once_with(cycle)

    def test_get_all_masters(self):
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.get_all_masters") as mck:
            tp.get_all_masters()
            mck.assert_called_once_with()

    def test_set_master(self, scenario):
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.set_master") as mck:
            tp.set_master(scenario)
            mck.assert_called_once_with(scenario)

    def test_compare_scenarios(self, scenario):
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.compare") as mck:
            tp.compare_scenarios(scenario, scenario, data_node_config_name="ds")
            mck.assert_called_once_with(scenario, scenario, data_node_config_name="ds")

    def test_subscribe_scenario(self, scenario):
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.subscribe") as mck:
            tp.subscribe_scenario(print)
            mck.assert_called_once_with(print, None)
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.subscribe") as mck:
            tp.subscribe_scenario(print, scenario=scenario)
            mck.assert_called_once_with(print, scenario)

    def test_unsubscribe_scenario(self, scenario):
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.unsubscribe") as mck:
            tp.unsubscribe_scenario(print)
            mck.assert_called_once_with(print, None)
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.unsubscribe") as mck:
            tp.unsubscribe_scenario(print, scenario=scenario)
            mck.assert_called_once_with(print, scenario)

    def test_subscribe_pipeline(self, pipeline):
        with mock.patch("taipy.pipeline.pipeline_manager.PipelineManager.subscribe") as mck:
            tp.subscribe_pipeline(print)
            mck.assert_called_once_with(print, None)
        with mock.patch("taipy.pipeline.pipeline_manager.PipelineManager.subscribe") as mck:
            tp.subscribe_pipeline(print, pipeline=pipeline)
            mck.assert_called_once_with(print, pipeline)

    def test_unsubscribe_pipeline(self, pipeline):
        with mock.patch("taipy.pipeline.pipeline_manager.PipelineManager.unsubscribe") as mck:
            tp.unsubscribe_pipeline(print)
            mck.assert_called_once_with(print, None)
        with mock.patch("taipy.pipeline.pipeline_manager.PipelineManager.unsubscribe") as mck:
            tp.unsubscribe_pipeline(print, pipeline=pipeline)
            mck.assert_called_once_with(print, pipeline)

    def test_delete_pipeline(self):
        with mock.patch("taipy.pipeline.pipeline_manager.PipelineManager.hard_delete") as mck:
            pipeline_id = PipelineId("pipeline_id")
            tp.delete_pipeline(pipeline_id)
            mck.assert_called_once_with(pipeline_id)

    def test_get_pipeline(self, pipeline):
        with mock.patch("taipy.pipeline.pipeline_manager.PipelineManager.get") as mck:
            pipeline_id = PipelineId("PIPELINE_id")
            tp.get(pipeline_id)
            mck.assert_called_once_with(pipeline_id)

    def test_get_pipelines(self):
        with mock.patch("taipy.pipeline.pipeline_manager.PipelineManager.get_all") as mck:
            tp.get_pipelines()
            mck.assert_called_once_with()

    def test_get_job(self):
        with mock.patch("taipy.job.job_manager.JobManager.get") as mck:
            job_id = JobId("JOB_id")
            tp.get(job_id)
            mck.assert_called_once_with(job_id)

    def test_get_jobs(self):
        with mock.patch("taipy.job.job_manager.JobManager.get_all") as mck:
            tp.get_jobs()
            mck.assert_called_once_with()

    def test_delete_job(self, task):
        with mock.patch("taipy.job.job_manager.JobManager.delete") as mck:
            job = Job(JobId("job_id"), task)
            tp.delete_job(job)
            mck.assert_called_once_with(job, False)
        with mock.patch("taipy.job.job_manager.JobManager.delete") as mck:
            job = Job(JobId("job_id"), task)
            tp.delete_job(job, False)
            mck.assert_called_once_with(job, False)
        with mock.patch("taipy.job.job_manager.JobManager.delete") as mck:
            job = Job(JobId("job_id"), task)
            tp.delete_job(job, True)
            mck.assert_called_once_with(job, True)

    def test_delete_jobs(self):
        with mock.patch("taipy.job.job_manager.JobManager.delete_all") as mck:
            tp.delete_jobs()
            mck.assert_called_once_with()

    def test_get_latest_job(self, task):
        with mock.patch("taipy.job.job_manager.JobManager.get_latest") as mck:
            tp.get_latest_job(task)
            mck.assert_called_once_with(task)

    def test_get_data_node(self, data_node):
        with mock.patch("taipy.data.data_manager.DataManager.get") as mck:
            tp.get(data_node.id)
            mck.assert_called_once_with(data_node.id)

    def test_get_data_nodes(self):
        with mock.patch("taipy.data.data_manager.DataManager.get_all") as mck:
            tp.get_data_nodes()
            mck.assert_called_once_with()

    def test_create_scenario(self, scenario):
        scenario_config = ScenarioConfig("scenario_config")
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.create") as mck:
            tp.create_scenario(scenario_config)
            mck.assert_called_once_with(scenario_config, None, None)
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.create") as mck:
            tp.create_scenario(scenario_config, datetime.datetime(2022, 2, 5))
            mck.assert_called_once_with(scenario_config, datetime.datetime(2022, 2, 5), None)
        with mock.patch("taipy.scenario.scenario_manager.ScenarioManager.create") as mck:
            tp.create_scenario(scenario_config, datetime.datetime(2022, 2, 5), "displayable_name")
            mck.assert_called_once_with(scenario_config, datetime.datetime(2022, 2, 5), "displayable_name")

    def test_create_pipeline(self):
        pipeline_config = PipelineConfig("pipeline_config")
        with mock.patch("taipy.pipeline.pipeline_manager.PipelineManager.get_or_create") as mck:
            tp.create_pipeline(pipeline_config)
            mck.assert_called_once_with(pipeline_config)

    def test_clean_all_entities(self, cycle):
        data_node_1_config = Config.add_data_node(name="d1", storage_type="in_memory", scope=Scope.SCENARIO)
        data_node_2_config = Config.add_data_node(
            name="d2", storage_type="pickle", default_data="abc", scope=Scope.SCENARIO
        )
        task_config = Config.add_task("my_task", data_node_1_config, print, data_node_2_config, scope=Scope.SCENARIO)
        pipeline_config = Config.add_pipeline("my_pipeline", task_config)
        scenario_config = Config.add_scenario("my_scenario", pipeline_config)
        CycleManager.set(cycle)

        scenario = ScenarioManager.create(scenario_config)
        ScenarioManager.submit(scenario)

        pickle_data_node = scenario.d2
        # Initial assertion
        assert isinstance(pickle_data_node, PickleDataNode)
        assert_file_exists(pickle_data_node.path)
        assert len(DataManager.get_all()) == 2
        assert len(TaskManager.get_all()) == 1
        assert len(PipelineManager.get_all()) == 1
        assert len(ScenarioManager.get_all()) == 1
        assert len(CycleManager.get_all()) == 1
        assert len(JobManager.get_all()) == 1

        # Test with clean entities disabled
        Config.set_global_config(clean_entities_enabled=False)
        success = Taipy.clean_all_entities()
        # Everything should be the same after clean_all_entities since clean_entities_enabled is False
        assert_file_exists(pickle_data_node.path)
        assert len(DataManager.get_all()) == 2
        assert len(TaskManager.get_all()) == 1
        assert len(PipelineManager.get_all()) == 1
        assert len(ScenarioManager.get_all()) == 1
        assert len(CycleManager.get_all()) == 1
        assert len(JobManager.get_all()) == 1
        assert not success

        # Test with clean entities enabled
        Config.set_global_config(clean_entities_enabled=True)
        success = Taipy.clean_all_entities()
        # File should not exist after clean_all_entities since clean_entities_enabled is True
        assert_file_not_exists(pickle_data_node.path)
        assert len(DataManager.get_all()) == 0
        assert len(TaskManager.get_all()) == 0
        assert len(PipelineManager.get_all()) == 0
        assert len(ScenarioManager.get_all()) == 0
        assert len(CycleManager.get_all()) == 0
        assert len(JobManager.get_all()) == 0
        assert success

    def test_clean_all_entities_with_user_pickle_files(self, pickle_file_path):
        user_pickle = PickleDataNode(
            config_name="d1", properties={"default_data": "foo", "path": pickle_file_path}, scope=Scope.SCENARIO
        )
        generated_pickle = PickleDataNode(config_name="d2", properties={"default_data": "foo"}, scope=Scope.SCENARIO)

        # File already exists so it does not write any
        assert len(DataManager.get_all()) == 1
        assert file_exists(user_pickle.path)
        assert_file_exists(generated_pickle.path)

        Config.set_global_config(clean_entities_enabled=True)
        Taipy.clean_all_entities()
        assert len(DataManager.get_all()) == 0
        assert_file_exists(user_pickle.path)
        assert_file_not_exists(generated_pickle.path)