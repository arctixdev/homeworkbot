<?php declare(strict_types=1);

namespace App\GraphQL\Mutations;

use App\Models\HomeworkProgress;

final readonly class SetHomeworkProgress
{
    /** @param  array{}  $args */
    public function __invoke(null $_, array $args)
    {
        $homeworkProgress = HomeworkProgress::query()->findOrFail($args['homework_id']);
        $homeworkProgress->update(['progress' => $args['progress']]);
        return $homeworkProgress;
    }
}
