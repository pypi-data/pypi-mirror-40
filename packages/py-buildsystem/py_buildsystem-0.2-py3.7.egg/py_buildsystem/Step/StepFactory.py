from Step.StepLink import StepLink
from Step.StepCompile import StepCompile


class StepFactory:
    @staticmethod
    def create(step_config, object_to_inject=None):
        step_type = list(step_config.keys())[0]

        if 'compile' in step_type:
            return StepCompile(step_config, object_to_inject.get_compiler())
        elif 'link' in step_type:
            return StepLink(step_config, object_to_inject.get_linker())
        else:
            raise TypeError('Unsuported step type')
