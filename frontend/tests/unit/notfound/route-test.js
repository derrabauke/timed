import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'

module('Unit | Route | notfound', function(hooks) {
  setupTest(hooks)

  test('exists', function(assert) {
    let route = this.owner.lookup('route:notfound')
    assert.ok(route)
  })
})
