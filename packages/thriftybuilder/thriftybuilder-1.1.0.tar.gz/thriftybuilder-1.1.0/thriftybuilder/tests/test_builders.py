import unittest

import itertools

from thriftybuilder.builders import DockerBuilder, CircularDependencyBuildError, UnmanagedBuildError, \
    InvalidDockerfileBuildError, BuildStepError
from thriftybuilder.storage import MemoryChecksumStorage
from thriftybuilder.tests._common import TestWithDockerBuildConfiguration, RUN_DOCKER_COMMAND
from thriftybuilder.tests._examples import EXAMPLE_IMAGE_NAME_2, EXAMPLE_IMAGE_NAME_1


class TestDockerBuilder(TestWithDockerBuildConfiguration):
    """
    Tests for `DockerBuilder`.
    """
    def setUp(self):
        super().setUp()
        self.checksum_storage = MemoryChecksumStorage()
        self.docker_builder = DockerBuilder(checksum_retriever=self.checksum_storage)

    def test_build_when_dockerfile_is_invalid(self):
        _, configuration = self.create_docker_setup(commands=["invalid"])
        self.docker_builder.managed_build_configurations.add(configuration)
        self.assertRaises(InvalidDockerfileBuildError, self.docker_builder.build, configuration)

    def test_build_when_build_fails(self):
        _, configuration = self.create_docker_setup(commands=[f"{RUN_DOCKER_COMMAND} exit 1"])
        self.docker_builder.managed_build_configurations.add(configuration)
        self.assertRaises(BuildStepError, self.docker_builder.build, configuration)

    def test_build_when_from_image_is_not_managed(self):
        _, configuration = self.create_docker_setup()
        assert configuration.identifier not in \
               itertools.chain(*(image.tags for image in self.docker_client.images.list()))
        self.assertRaises(UnmanagedBuildError, self.docker_builder.build, configuration)

    def test_build_when_from_image_is_managed(self):
        configurations = self.create_dependent_docker_build_configurations(4)
        self.docker_builder.managed_build_configurations.add_all(configurations)
        self.docker_builder.managed_build_configurations.add(self.create_docker_setup()[1])

        build_results = self.docker_builder.build(configurations[-1])
        self.assertCountEqual(
            {configuration: configuration.identifier for configuration in configurations}, build_results)

    def test_build_when_circular_dependency(self):
        configurations = [
            self.create_docker_setup(image_name=EXAMPLE_IMAGE_NAME_1, from_image_name=EXAMPLE_IMAGE_NAME_2)[1],
            self.create_docker_setup(image_name=EXAMPLE_IMAGE_NAME_2, from_image_name=EXAMPLE_IMAGE_NAME_1)[1]]
        self.docker_builder.managed_build_configurations.add_all(configurations)
        self.assertRaises(CircularDependencyBuildError, self.docker_builder.build_all)

    def test_build_when_up_to_date(self):
        _, configuration = self.create_docker_setup()
        self.docker_builder.managed_build_configurations.add(configuration)
        self.checksum_storage.set_checksum(
            configuration.identifier, self.docker_builder.checksum_calculator.calculate_checksum(configuration))

        build_results = self.docker_builder.build(configuration)
        self.assertEqual(0, len(build_results))

    def test_build_all_when_none_managed(self):
        built = self.docker_builder.build_all()
        self.assertEqual(0, len(built))

    def test_build_all_when_one_fails(self):
        configurations = self.create_dependent_docker_build_configurations(4)
        configurations += [self.create_docker_setup(commands=[f"{RUN_DOCKER_COMMAND} exit 1"])[1]]
        self.docker_builder.managed_build_configurations.add_all(configurations)
        self.assertRaises(BuildStepError, self.docker_builder.build_all)

    def test_build_all_when_managed(self):
        configurations = self.create_dependent_docker_build_configurations(4)
        self.docker_builder.managed_build_configurations.add_all(configurations)

        build_results = self.docker_builder.build_all()
        self.assertCountEqual(
            {configuration: configuration.identifier for configuration in configurations}, build_results)

    def test_build_all_when_some_up_to_date(self):
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
        configurations = self.create_dependent_docker_build_configurations(4)
        self.docker_builder.managed_build_configurations.add_all(configurations)

        build_results = self.docker_builder.build(configurations[1])
        assert len(build_results) == 2

        for configuration in build_results.keys():
            checksum = self.docker_builder.checksum_calculator.calculate_checksum(configuration)
            self.checksum_storage.set_checksum(configuration.identifier, checksum)

        build_results = self.docker_builder.build_all()
        self.assertCountEqual(configurations[2:], build_results)

    def test_build_when_from_image_updated(self):
        configurations = self.create_dependent_docker_build_configurations(2)
        self.docker_builder.managed_build_configurations.add_all(configurations)

        build_results = self.docker_builder.build_all()
        assert len(build_results) == 2

        for configuration in build_results.keys():
            checksum = self.docker_builder.checksum_calculator.calculate_checksum(configuration)
            self.checksum_storage.set_checksum(configuration.identifier, checksum)

        parent_image = configurations[0]

        with open(parent_image.dockerfile_location, "a") as file:
            file.write(f"{RUN_DOCKER_COMMAND} echo 1")
        parent_image.reload()

        build_results = self.docker_builder.build_all()
        self.assertEqual(2, len(build_results))


if __name__ == "__main__":
    unittest.main()
