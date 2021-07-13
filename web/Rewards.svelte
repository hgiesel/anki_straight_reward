<script>
    const {
        TitledContainer,
        SpinBoxRow,
        SpinBoxFloatRow,
        SwitchRow,
    } = anki.components;

    export let data;
</script>

<TitledContainer title="Rewards">
    <SpinBoxRow
        bind:value={$data.straightLength}
        defaultValue={2}
        markdownTooltip="Length of what is considered a straight success. Starting at this length, ease rewards will be applied. The value 0 is the same as deactivating Straight Rewards."
    >
        Begin at straight of length
    </SpinBoxRow>

    <SpinBoxFloatRow
        bind:value={$data.baseEase}
        defaultValue={0.05}
        markdownTooltip="The ease reward is calculated as: BaseEase + StepEase ⋅ (StraightLength - RequiredStraightLength)"
    >
        Base ease reward
    </SpinBoxFloatRow>

    <SpinBoxFloatRow
        bind:value={$data.stepEase}
        defaultValue={0.05}
        markdownTooltip="The ease reward is calculated as: BaseEase + StepEase ⋅ (StraightLength - RequiredStraightLength)"
    >
        Step ease reward
    </SpinBoxFloatRow>

    <SpinBoxFloatRow
        bind:value={$data.startEase}
        defaultValue={1.30}
        markdownTooltip="Only cards with an ease factor between (inclusive) *Start Ease* and *Stop Ease* are considered for ease rewards."
    >
        Start at ease
    </SpinBoxFloatRow>

    <SpinBoxFloatRow
        bind:value={$data.stopEase}
        defaultValue={2.50}
        markdownTooltip="Only cards with an ease factor between (inclusive) *Start Ease* and *Stop Ease* are considered for ease rewards."
    >
        Stop at ease
    </SpinBoxFloatRow>

    <SwitchRow
        bind:value={$data.enableNotification}
        defaultValue={true}
        markdownTooltip="Enable or disable the notifications that arise during review."
    >
        Enable notification
    </SwitchRow>
</TitledContainer>
